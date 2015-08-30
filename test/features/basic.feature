Feature: Basic recipy use

Scenario: Run a simple test
    Given we have recipy set up for testing
    When we run some code
    Then an entry should be added to the database

Scenario: Test running recipy as a module
	Given we have recipy set up for testing
	When we run some code as a module
	Then an entry should be added to the database