# Mario

[![Build Status](https://travis-ci.org/best-doctor/Mario.svg?branch=master)](https://travis-ci.org/best-doctor/Mario)
[![Maintainability](https://api.codeclimate.com/v1/badges/86b3c0549c660bda7f4f/maintainability)](https://codeclimate.com/github/best-doctor/Mario/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/86b3c0549c660bda7f4f/test_coverage)](https://codeclimate.com/github/best-doctor/Mario/test_coverage)
[![PyPI version](https://badge.fury.io/py/super-mario.svg)](https://badge.fury.io/py/super-mario)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/super-mario)
Library for separating data input, output and processing in your business application.

![Mario](https://raw.githubusercontent.com/best-doctor/Mario/master/docs_imgs/mario.png)

**Disclaimer**: the library is sooo pre-alpha.

## Installation

`pip install super-mario`

## Usage example

```python
class VisitHistoryView(BasePipeline):
    pipeline = [
        'get_user_bills',
        'get_user_legals',
        'calculate_visits_periods',
        'format_json_response',
    ]

    @input_pipe
    def get_user_bills(user: User) -> List[UserBill]:  # User and UserBill is a Python dataclass
        """
        Returns list of python dataclasses, that represents information about user bills.
        
        - no business logic on this layer (use linters for detect high complexity level)
        - we can use database access on this layer, but only through special context manager 
        - here we have special model manager that returns simple dataclass, not an orm instance
        - we take `user` arguments from base context, that was filled by PipelineView
        - we have no access to base context from any method
        """
        return UserBill.objects_to_dataclass.get_user_bills(user)

    @process_pipe
    def calculate_visits_periods(user_bills: List[UserBill]) -> List[VisitsPeriods]:
        """
        VisitsPeriods is a business logic hadler.
        
        - we can't use database access on this layer
        - it's a domain entity
        - it has no ability to interact with external dependencies
        - when we change something in outer world, we should not make any change in this layer
        - also, we should have here the best code. This code should be tested very well
        """
        return VisitsPeriods.calculate(patient_bills)

    @output_pipe
    def get_pipeline_result(visits_periods: List[VisitsPeriodsDataClass]) -> JsonResponse:
        """
        Representation layer.
    
        - we can use database access on this layer, but only through special context manager
        - it also takes dataclasses
        - no business logic on this layer (use linters for detect high complexity level)
        """
        return {'visit_periods': visits_periods}
``` 
