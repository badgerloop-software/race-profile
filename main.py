from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
import uvicorn
import time
import logging
from data_pipeline.simulinkPlugin.config import constants
import matlab.engine
import numpy as np
from data_pipeline.dataExtract import extractVars, NearestKeyDict
from data_pipeline.dataProcess import dataProcess
from data_pipeline.simulinkPlugin import plugin
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define FastAPI app
# We will add event handlers instead of using lifespan directly on init
app = FastAPI()

# Store results globally
api_results = [
    {"max_distance": "Pending..."},
    {"optimized_power": "Pending..."}
]

# --- Define startup/shutdown event functions ---
async def startup_event():
    """Handles application startup logic."""
    logger.info("--- Startup Event Handler Triggered ---")
    # Start MATLAB Engine here
    logger.info("--- Startup Event: Starting MATLAB engine... ---")
    try:
        plugin.start_matlab_engine()
        logger.info("--- Startup Event: MATLAB engine started successfully ---")
    except Exception as engine_err:
        logger.error("--- Startup Event: FAILED to start MATLAB engine: %s ---", engine_err, exc_info=True)
        plugin.eng = None # Ensure plugin.eng is None if start failed

    # Start the optimization task in the background only if engine started
    if plugin.eng:
        logger.info("--- Startup Event: Creating background task ---")
        task = asyncio.create_task(run_optimization_background())
        # Store task in app state if needed for shutdown cancellation
        app.state.optimization_task = task
        logger.info("--- Startup Event: Background task created ---")
    else:
        logger.warning("--- Startup Event: Skipping background task creation due to MATLAB engine failure ---")
        api_results[:] = [
            {"max_distance": "Engine Error at Startup"},
            {"optimized_power": "Engine Error at Startup"}
        ]
    logger.info("--- Startup Event Handler Finished ---")


async def shutdown_event():
    """Handles application shutdown logic."""
    logger.info("--- Shutdown Event Handler Triggered ---")
    # Optional: Add logic to wait for or cancel the task
    # if hasattr(app.state, 'optimization_task') and not app.state.optimization_task.done():
    #     logger.info("--- Shutdown Event: Cancelling background task ---")
    #     app.state.optimization_task.cancel()
    #     try:
    #         await app.state.optimization_task
    #     except asyncio.CancelledError:
    #         logger.info("--- Shutdown Event: Background task cancelled ---")
    #     except Exception as e:
    #         logger.error("--- Shutdown Event: Error during task cancellation/await: %s ---", e)

    logger.info("--- Shutdown Event: Closing MATLAB Engine ---")
    try:
        if plugin.eng:
            plugin.close_workspace()
            logger.info("--- Shutdown Event: MATLAB Engine Closed ---")
        else:
            logger.info("--- Shutdown Event: MATLAB Engine was not running, skipping close ---")
    except Exception as close_err:
        logger.error("--- Shutdown Event: Error closing MATLAB Engine: %s ---", close_err, exc_info=True)
    logger.info("--- Shutdown Event Handler Finished ---")

# Register the event handlers with the app
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


@app.get("/strategy")
async def strategy_results():
    """Returns the latest optimization results."""
    logger.info("Serving /strategy endpoint: %s", api_results)
    return api_results

# --- _run_matlab_sync and run_optimization_background functions remain the same ---
def _run_matlab_sync():
    """Synchronous function containing the MATLAB optimization logic."""
    logger.info("--- Starting Synchronous MATLAB Optimization ---")
    start_time = time.time()
    global api_results # Ensure we modify the global variable

    # Setup constants
    constants.update({"initialguess": 500})

    # MATLAB Engine and Optimization
    if plugin.eng:
        logger.info("MATLAB engine available, loading constants...")
        plugin.load_constants()
        start_optimize = time.time()
        try:
            # Run optimization
            logger.info("Starting optimization...")
            maxDistance, optimizedPower = plugin.run_optimization()

            api_results[:] = [
                {"max_distance": "Optimization Running..."},
                {"optimized_power": "Optimization Running..."}
            ]

            end_optimize = time.time()
            logger.info("Optimization finished in %.2f seconds.", end_optimize - start_optimize)
            logger.info("Max Distance: %s", maxDistance)
            logger.info("Optimized Power: %s", optimizedPower)

            # Update results
            api_results[:] = [
                {"max_distance": maxDistance},
                {"optimized_power": optimizedPower}
            ]
            logger.info("Updated api_results: %s", api_results)
        except Exception as opt_error:
            logger.error("Error during optimization: %s", opt_error, exc_info=True)
            api_results[:] = [
                {"max_distance": "Error"},
                {"optimized_power": "Error"}
            ]
    else:
        logger.error("MATLAB engine not available. Skipping optimization.")
        api_results[:] = [
            {"max_distance": "Engine Error"},
            {"optimized_power": "Engine Error"}
        ]

    end_time = time.time()
    logger.info("--- Synchronous MATLAB Optimization Completed in %.2f seconds ---", end_time - start_time)


async def run_optimization_background():
    """Runs the MATLAB optimization in a separate thread."""
    logger.info("--- Entered run_optimization_background ---")
    try:
        logger.info("--- Preparing to run _run_matlab_sync in thread ---")
        await asyncio.to_thread(_run_matlab_sync)
        logger.info("--- _run_matlab_sync thread finished ---")
        logger.info("--- Background Optimization Task Finished ---")
    except Exception as e:
        logger.error("--- Error in Background Optimization Task: %s ---", e, exc_info=True)
        api_results[:] = [
            {"max_distance": "Task Error"},
            {"optimized_power": "Task Error"}
        ]
    logger.info("--- Exiting run_optimization_background ---")

# --- Lifespan context manager is NOT used in this version ---
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     ...
# app.lifespan = lifespan # This line is removed/commented

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    plugin.eng = None # Ensure engine is None initially
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # #Run the sumulation and time how long it takes.
    # # Create simulator instance
    # simulator = CarSimulator()

    # # Then use it where needed
    # results = simulator.run_simulation(target_speed=20, target_power=500)

    #With the total time the first simuation took, query the corresponsing data from redis and do data process to remove outliers and copmute means.

    #Feed new values into simulation and run again.

    #Repeat.

    #Every 30 minutes, when the car it leaves certain radius distance, all of the weather data queryed from the API is irrelavant. 
    #So we pull the predicted distance travelled, and look up the approximate position in the lookup table, and feed that position into the API function and feed the resulting irridance data into the simulation.
    #SOC, Pack_power, ghi, cloud_opacity.
    #When we look up weather data, our total irridance will be the Global Horizontal Irridance (ghi) multiplied by the Cloud Opacity(cloud_opacity).
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
    #Obtaining weather data from the Grand Canyon
    #get_weather_data(36.099763, -112.112485, 5)
    #extractVars.launch_live_graph()

    # extracted_variables = extractVars.record_multiple_data(3, input_variables)
    # means = dprocess.process_recorded_values(extracted_variables, input_variables)

    # print(type(means))
    # print(means)

    # df = pd.read_csv("solar_car_telemetry/src/solcast/output.csv")
    # print(df)