# Race Strategy
We are building a solar  race car, and we want to drive wisely. Thus came the ultimate mission of the race strategy team: we find the **optimal driving strategy** to unleash the car's full potential.

These are the following things that are a work-in-progress:

**Model Validation:** We need to show our model to each subteam and discuss if we are doing a faithful simulation of their part of the system.

**Python Conversion:** We have built the model in Simulink, but in the long run, it may be more beneficial if we convert our model into Python. Given the current size of our model, this would be a big task, and we need to collaborate with Software on this. The motivation is mainly twofold: 

It would make the integration between our model and telemetry API easier, and, hopefully, pave the way for real-time simulation prediction. 

It would give us more transparency and control over the project, yielding space for debugging and optimization. This is especially important as the complexity of our model grows.

**Integration with telemetry data:** We need to be able to give valid predictions based on how our car is doing now. We need to hook our simulation up with real-time data on the physical car so that it can be upgrated into a closed-loop feedback system. I anticipate a collaboration with the software team on this project.

**Optimization Algorithm:** Now that we have an idea on how the car runs given different conditions, how do we find the optimal race strategy? Our ultimate goal is to have the confidence to tell the driver to drive at a certain speed at a certain location, so that we keep a good balance between battery consumption and distance coverage, while considering physical constrains and weather prediction for the next several hours.

**Fine-tuning:** We still need to match the simulated car to the actual car. This means that we need to analyze data from future test drives and retrieve parameters for our model. Since we are building a new car simultaneously, this would not be our main focus this semester. However, it would still be helpful to work with Mechanical to come up with a better methodology for test-drive data analysis.