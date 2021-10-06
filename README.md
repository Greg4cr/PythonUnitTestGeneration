# PythonUnitTestGeneration

A simple unit test input generator for Python. This code corresponds to the chapter on unit testing in the upcoming book "Optimising the Software Development Process with Artificial Intelligence".

A pre-print of this chapter is available in the file `chapter.pdf`.

This tool is written targeting Python 3.6, and will not function properly under Python 2. 

# Installation 

This tool requires the `pytest` and `pytest-cov` packages.

In the `src/` folder, run `pip3 install -r requirements.txt` to install all dependencies.

Note that in Debian-based Linux distributions, such as Ubuntu, you may need to separately install the `python-pytest` and `python-pytest-cov` packages. You may do so by running the following commands:

`sudo apt install python-pytest`

`sudo apt install python-pytest-cov`

# Execution

We offer both a hill climber and a genetic algorithm. In either case, the class under test must have a metadata JSON file. For the included BMI example, the class-under-test is located in `src/example/bmi_claculator.py` and the metadata JSON is located at `src/example/BMICalc_metadata.json`.

To execute test generation, choose your desired generation algorithm and set your desired values for the command line parameters.

`python3 genetic_algorithm.py [parameters]`

The parameters that can be set for the genetic algorithm include:

- -m <metadata file location (default points to BMI example)> 
- -g <search budget, the maximum number of generations before printing the best solution found (default: 200)>
- -p <population size (default: 20)>
- -s <tournament size, for selection (default: 6)>
- -t <mutation probability (default: 0.7)>
- -x <crossover probability (default: 0.7)>
- -o <crossover operator (choices: single, uniform (default))>
- -e <number of generations before search terminates due to lack of improvement (default: 30)>
- -c <maximum number of test cases in a randomly-generated test suite (default: 20)>
- -a <maxmium number of actions (variable assignments, method calls) in a randomly-generated test case (default: 20)>
- -z <test suite size penalty (default: 10)>
- -l <test case length penalty (default: 30)>

`python3 hill_climber.py [parameters]`

The parameters that can be set for the hill climber include:

- -m <metadata file location (default points to BMI example)> 
- -g <search budget, the maximum number of generations before printing the best solution found (default: 200)>
- -t <maximum number of mutations tried before restarting the search (default: 500)>
- -r <maximum number of restarts (default: 5)>
- -c <maximum number of test cases in a randomly-generated test suite (default: 20)>
- -a <maxmium number of actions (variable assignments, method calls) in a randomly-generated test case (default: 20)>
- -z <test suite size penalty (default: 10)>
- -l <test case length penalty (default: 30)>

Explanation of the two techniques and the parameters can be found in the book chapter.
