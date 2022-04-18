# metaflow_magicdir
> Save Entire Directories Into Metaflow's Metadata Store


## Install

`pip install metaflow_magicdir`

## How to use

You can use `@magicdir` to pass local directories between metaflow steps.  This will also work remotely.

```python
# examples/example_flow.py

from metaflow import FlowSpec, step
from metaflow_magicdir import magicdir


class MagicDirFlow(FlowSpec):

    @magicdir(dir='mydir')
    @step
    def start(self):
        with open('mydir/output1', 'w') as f:
            f.write('hello world')
        with open('mydir/output2', 'w') as f:
            f.write('hello world again')
        self.next(self.end)

    @magicdir(dir='mydir')
    @step
    def end(self):
        print('first', open('mydir/output1').read())
        print('second', open('mydir/output1').read())

if __name__ == "__main__":
    MagicDirFlow()
```

If you run the above flow, you will see the following output:

> python examples/example_flow.py run

```
Metaflow 2.5.4 executing MagicDirFlow for user:hamelValidating your flow...
    The graph looks good!
Running pylint...
    Pylint is happy!
2022-04-18 13:53:24.077 Workflow starting (run-id 1650315204073458):
2022-04-18 13:53:24.083 [1650315204073458/start/1 (pid 13299)] Task is starting.
2022-04-18 13:53:24.834 [1650315204073458/start/1 (pid 13299)] Task finished successfully.
2022-04-18 13:53:24.840 [1650315204073458/end/2 (pid 13302)] Task is starting.
2022-04-18 13:53:25.527 [1650315204073458/end/2 (pid 13302)] first hello world
2022-04-18 13:53:25.608 [1650315204073458/end/2 (pid 13302)] second hello world
2022-04-18 13:53:25.609 [1650315204073458/end/2 (pid 13302)] Task finished successfully.
2022-04-18 13:53:25.610 Done!
```

You can retrieve the results from the above Flow with the client api and `extract_magicdir`:

Let's first remove the directory if it exists:

```python
!rm -rf mydir/ #remove the directory if it exists
```

```python
from metaflow import Flow
from metaflow_magicdir import extract_magicdir
run_data = Flow('MagicDirFlow').latest_successful_run.data
extract_magicdir(run_data)
```

We can now inspect the contents of this directory to see it's contents!

```python
!ls mydir/
```

    output1 output2


### `magicdir` with `foreach`

Nothing special is required to use `magicdir` with foreach.  Consider the following modification to the above flow:

```python
#examples/mapflow.py

from metaflow import FlowSpec, step
from metaflow_magicdir import magicdir


class MagicDirMapFlow(FlowSpec):
    """Show how magic directories work with foreach"""

    @step
    def start(self):
        self.step_num = range(5)
        self.next(self.write, foreach='step_num')

    @magicdir(dir='my_map_dir')
    @step
    def write(self):
        self.step_idx = self.input # metaflow gives self.input a value from `step_num` from the prior step
        with open(f'my_map_dir/{self.step_idx}.txt', 'w') as f:
            f.write(f'this is step {self.step_idx}')
        self.next(self.read)

    @magicdir(dir='my_map_dir')
    @step
    def read(self):
        print('file contents:', open(f'my_map_dir/{self.step_idx}.txt').read())
        self.next(self.join)
    
    @step
    def join(self, inputs):
        print(f"step numbers were: {[i.step_idx for i in inputs]}")
        self.next(self.end)

    @step
    def end(self): pass

if __name__ == "__main__":
    MagicDirMapFlow()

if __name__ == "__main__":
    MagicDirMapFlow()
```

> python examples/mapflow.py run

```
Metaflow 2.5.4 executing MagicDirMapFlow for user:hamelValidating your flow...
    The graph looks good!
Running pylint...
    Pylint is happy!
2022-04-18 13:41:56.687 Workflow starting (run-id 1650314516684584):
2022-04-18 13:41:56.695 [1650314516684584/start/1 (pid 12420)] Task is starting.
2022-04-18 13:41:57.444 [1650314516684584/start/1 (pid 12420)] Foreach yields 5 child steps.
2022-04-18 13:41:57.445 [1650314516684584/start/1 (pid 12420)] Task finished successfully.
2022-04-18 13:41:57.452 [1650314516684584/write/2 (pid 12423)] Task is starting.
2022-04-18 13:41:57.459 [1650314516684584/write/3 (pid 12424)] Task is starting.
2022-04-18 13:41:57.466 [1650314516684584/write/4 (pid 12425)] Task is starting.
2022-04-18 13:41:57.473 [1650314516684584/write/5 (pid 12426)] Task is starting.
2022-04-18 13:41:57.481 [1650314516684584/write/6 (pid 12427)] Task is starting.
2022-04-18 13:41:58.438 [1650314516684584/write/3 (pid 12424)] Task finished successfully.
2022-04-18 13:41:58.450 [1650314516684584/read/7 (pid 12438)] Task is starting.
2022-04-18 13:41:58.452 [1650314516684584/write/2 (pid 12423)] Task finished successfully.
2022-04-18 13:41:58.463 [1650314516684584/read/8 (pid 12439)] Task is starting.
2022-04-18 13:41:58.465 [1650314516684584/write/5 (pid 12426)] Task finished successfully.
2022-04-18 13:41:58.473 [1650314516684584/read/9 (pid 12440)] Task is starting.
2022-04-18 13:41:58.478 [1650314516684584/write/6 (pid 12427)] Task finished successfully.
2022-04-18 13:41:58.487 [1650314516684584/read/10 (pid 12441)] Task is starting.
2022-04-18 13:41:58.489 [1650314516684584/write/4 (pid 12425)] Task finished successfully.
2022-04-18 13:41:58.496 [1650314516684584/read/11 (pid 12442)] Task is starting.
2022-04-18 13:41:59.314 [1650314516684584/read/7 (pid 12438)] file contents: this is step 1
2022-04-18 13:41:59.348 [1650314516684584/read/8 (pid 12439)] file contents: this is step 0
2022-04-18 13:41:59.350 [1650314516684584/read/9 (pid 12440)] file contents: this is step 3
2022-04-18 13:41:59.362 [1650314516684584/read/11 (pid 12442)] file contents: this is step 2
2022-04-18 13:41:59.370 [1650314516684584/read/10 (pid 12441)] file contents: this is step 4
2022-04-18 13:41:59.450 [1650314516684584/read/7 (pid 12438)] Task finished successfully.
2022-04-18 13:41:59.479 [1650314516684584/read/9 (pid 12440)] Task finished successfully.
2022-04-18 13:41:59.482 [1650314516684584/read/8 (pid 12439)] Task finished successfully.
2022-04-18 13:41:59.495 [1650314516684584/read/10 (pid 12441)] Task finished successfully.
2022-04-18 13:41:59.497 [1650314516684584/read/11 (pid 12442)] Task finished successfully.
2022-04-18 13:41:59.505 [1650314516684584/join/12 (pid 12459)] Task is starting.
2022-04-18 13:42:00.183 [1650314516684584/join/12 (pid 12459)] step numbers were: [0, 3, 2, 1, 4]
2022-04-18 13:42:00.261 [1650314516684584/join/12 (pid 12459)] Task finished successfully.
2022-04-18 13:42:00.269 [1650314516684584/end/13 (pid 12462)] Task is starting.
2022-04-18 13:42:01.027 [1650314516684584/end/13 (pid 12462)] Task finished successfully.
2022-04-18 13:42:01.027 Done!
```
