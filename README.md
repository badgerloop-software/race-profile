# The Goal of Race Strategy

We are building a race car, and we want to drive wisely. Thus came the ultimate mission of the race strategy team: we find the **optimal driving strategy** to unleash the car's full potential. 

## Tools for Race Strategy

### Matlab, Simulink, and Physical Intuitions 
In the quest to study the dynamics and behavior of the car, we are building a simulated model of our solar car using Simulink on Matlab.

Personally, Simulink is fairly easy to get started (it's kinda like Scratch). Matlab on the other hand is both interesting and frustrating, so one would need a fair fluency in the language, as well as a good temper.

The model of the car is built on models of each small section, and their interaction. We mainly follow the physics of each piece in building the model, and a trustworthy physical intuition.

### Python, and a Clear Mind for Data Analysis
We need parameters to fine-tune our model so that it matches the behavior of the actual car. We do this by analyzing data from test drives. 

Historically, Python and Matlab were both used for data analysis, so a fair fluency in either language would suffice.

## The Dichotomy of Race Strategy System

### The Simulation
As mentioned above, our simulation involves a model of the solar car. But that's not all to it. To study the car's behavior in different environments and weather, we have to also consider external conditions and their impact on the car. The overall simulation can be broken down into two big parts:
1. Interaction among different components of the car
2. The Car's response to external conditions

The simulation can be found on our github repo.

### Current Projects

- ✅ **Model Validation:** We need to show our model to each subteam and discuss if we are doing a faithful simulation of their part of the system.

- 🔄 **Data Pipeline:** We need to be able to give valid predictions based on how our car is doing in realtime. We need to hook our simulation up with real-time data on the physical car so that it can be upgraded into a closed-loop feedback system. [Dedicated page: Data Pipeline and Model Integration]

- 🎯 **The Optimizer:** Now that we have an idea on how the car runs given different conditions, how do we find the optimal race strategy? Our ultimate goal is to have the confidence to tell the driver to drive at a certain speed at a certain location, so that we keep a good balance between battery consumption and distance coverage, while considering physical constraints and weather prediction for the next several hours. [Dedicated page: The Optimizer]

- ⏳ **Fine-tuning:** (non-priority) We still need to match the simulated car to the actual car. This means that we need to analyze data from future test drives and retrieve parameters for our model. Since we are building a new car simultaneously, this would not be our main focus this semester. However, it would still be helpful to work with Mechanical to come up with a better methodology for test-drive data analysis.
