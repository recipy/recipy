Feature: Basic recipy use

Scenario: Run a script with recipy imported
	When we run some code
	Then an entry should be added to the database
	And it should have a recorded exit date

Scenario: Run a script with recipy on the commandline
	When we run some code as a module
	Then an entry should be added to the database

Scenario: Run a script with data hashing
	Given the user opted in to hash data
	When we run some code
	Then each output should have a SHA-1 hash
