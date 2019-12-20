# Mario docs

## Terminology

**Pipe** – single action with data eg fetching, processing or output.
Receives some data as input and optionally returns some new data.
Each pipe should do single logical step of data processing.

**Pipeline** – sequential set of pipes, that receives some data,
process it with set of pipes and do some scenario.

## Idea

Pipelines helps you to separate long scenario to sequential
set of small actions to make code more descriptive, understandable
and testable.

Each pipe has its own type, has access only to data it uses, it can't 
overwrite or modify existing data. Pipes should be short and represent
single logic step of scenario.

All pipes are staticmethods and has no access to pipeline object or class.
Even if pipe has no `@staticmethod` decorator, it is static.
You can also specify `@staticmethod` for explicitness.

Pipes returns dict with named data objects, that can be injected in
other pipes.

Data transferred between pipes via data injection and only in simple types:
no class instances, ORM objects, etc. Only list, tuples, dicts, ints,
strings and so on.

## Pipe types

**Input** pipes should be used to receive data. It should not do
any data processing, only receiving. Should not do any data updates,
only reading. Preferably to use read-only access to data storages.  

**Process** pipes do data processing: transferring one data to another.
No fetch or output, only processing. Can have logic, but should be
[pure](https://en.wikipedia.org/wiki/Pure_function).

**Output** pipes are used to send data somewhere: write to database,
send to messenger, etc. Should not have any logic inside and should
be very non-complex.

## Pipe creating example

1. Make class, inherited from `BasePipeline`.

```python
from super_mario import BasePipeline

class ExamplePipeline(BasePipeline):
    pass
```

2. Fill `pipeline` with sequential names of pipes.

```python
from super_mario import BasePipeline

class ExamplePipeline(BasePipeline):
    pipeline = ['sum_numbers', 'multiply_numbers']
```

3. Add pipes. Each pipe should have pipe type decorator,
required arguments and optionally return new data.

```python
from super_mario import BasePipeline, process_pipe, output_pipe

class ExamplePipeline(BasePipeline):
    pipeline = ['sum_numbers', 'multiply_numbers', 'send_to_slack']
    
    @process_pipe
    @staticmethod
    def sum_numbers(a, b):
        return {'d': a + b}

    @process_pipe
    @staticmethod
    def multiply_numbers(c, d):
        return {'e': c * d}

    @output_pipe
    @staticmethod
    def send_to_slack(e):
        send_message_to_slack(text=e)

```

4. Run pipe with all specified arguments:

```python
ExamplePipeline.run(a=1, b=2, c=3)
```

## Pipeline validation

Some validations are made in runtime with `BasePipeline`, such as all pipes
has realization, no pipes overwrite data, etc.
Watch out for `ProgrammingException` errors.

Some other validations are done as static analysis,
so please use [flake8-super-mario](https://github.com/Melevir/flake8-super-mario).
Mario doesn't make a lot of sence without these validations.


## Pipeline logging

Pipelines has logging that is nice for debugging and development.
To enable it, set `super-mario` logger to debug level.
All debug pipeline info will passed to stdout.
