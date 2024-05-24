# Trophallaxis_Mesa_Discrete

## Summary

A simplified agent based model of honey bee movement and food exchange behavior via *trophallaxis*. The model adapts the Netlogo model created by [ggfard](https://github.com/ggfard/Trophallaxis_ABM/commits?author=ggfard), to utilize the [Mesa library](https://github.com/projectmesa) and runs in Python.  

The agent's movement follows the excluded volume rule, whereby agents cannot overlap at any time during the simulation. Initial fed agents (foragers who have food to share) are shown in red and hungry agents are black. As the model progresses, agents move while exchanging food when they come into contact. The model ends once food is distributed almost evenly between all agents.

## How to Run

Make sure to install the Mesa Python library
~~~
pip install mesa --quiet
~~~

Once all dependencies are installed, run the model using the following command, which will launch an interactive server:
~~~
$  python run.py
~~~
