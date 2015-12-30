Feature: Basic recipy use

Scenario: Run a script with recipy imported
	When we run some code
	Then an entry should be added to the database

Scenario: Run a script with recipy on the commandline
	When we run some code as a module
	Then an entry should be added to the database
