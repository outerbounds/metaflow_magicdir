# metaflow_magicdir
> Save Entire Directories Into Metaflow's Metadata Store


## Install

`pip install metaflow_magicdir`

## How to use

You can use `@magicdir` to pass local directories between metaflow steps.  This will also work remotely.

```
%%writefile examples/example_flow.py

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

    Overwriting examples/example_flow.py


If you run the above flow, you will see the following output:

```
!python examples/example_flow.py run
```

    [35m[1mMetaflow 2.5.4[0m[35m[22m executing [0m[31m[1mMagicDirFlow[0m[35m[22m[0m[35m[22m for [0m[31m[1muser:hamel[0m[35m[22m[K[0m[35m[22m[0m
    [35m[22mValidating your flow...[K[0m[35m[22m[0m
    [32m[1m    The graph looks good![K[0m[32m[1m[0m
    [35m[22mRunning pylint...[K[0m[35m[22m[0m
    [32m[1m    Pylint is happy![K[0m[32m[1m[0m
    [35m2022-04-18 13:40:59.728 [0m[1mWorkflow starting (run-id 1650314459725082):[0m
    [35m2022-04-18 13:40:59.734 [0m[32m[1650314459725082/start/1 (pid 12408)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:00.472 [0m[32m[1650314459725082/start/1 (pid 12408)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:00.479 [0m[32m[1650314459725082/end/2 (pid 12412)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:01.161 [0m[32m[1650314459725082/end/2 (pid 12412)] [0m[22mfirst hello world[0m
    [35m2022-04-18 13:41:01.245 [0m[32m[1650314459725082/end/2 (pid 12412)] [0m[22msecond hello world[0m
    [35m2022-04-18 13:41:01.246 [0m[32m[1650314459725082/end/2 (pid 12412)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:01.247 [0m[1mDone![0m
    [0m

You can retrieve the results from the above Flow with the client api and `extract_magicdir`:

Let's first remove the directory if it exists:

```
!rm -rf mydir/ #remove the directory if it exists
```

```
from metaflow import Flow
from metaflow_magicdir import extract_magicdir
run_data = Flow('MagicDirFlow').latest_successful_run.data
extract_magicdir(run_data)
```

We can now inspect the contents of this directory to see it's contents!

```
!ls mydir/
```

    output1 output2


### `magicdir` with `foreach`

Nothing special is required to use `magicdir` with foreach.  Consider the following modification to the above flow:

```
%%writefile examples/mapflow.py

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

    Overwriting examples/mapflow.py


```
!python examples/mapflow.py run
```

    [35m[1mMetaflow 2.5.4[0m[35m[22m executing [0m[31m[1mMagicDirMapFlow[0m[35m[22m[0m[35m[22m for [0m[31m[1muser:hamel[0m[35m[22m[K[0m[35m[22m[0m
    [35m[22mValidating your flow...[K[0m[35m[22m[0m
    [32m[1m    The graph looks good![K[0m[32m[1m[0m
    [35m[22mRunning pylint...[K[0m[35m[22m[0m
    [32m[1m    Pylint is happy![K[0m[32m[1m[0m
    [35m2022-04-18 13:41:56.687 [0m[1mWorkflow starting (run-id 1650314516684584):[0m
    [35m2022-04-18 13:41:56.695 [0m[32m[1650314516684584/start/1 (pid 12420)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:57.444 [0m[32m[1650314516684584/start/1 (pid 12420)] [0m[1mForeach yields 5 child steps.[0m
    [35m2022-04-18 13:41:57.445 [0m[32m[1650314516684584/start/1 (pid 12420)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:57.452 [0m[32m[1650314516684584/write/2 (pid 12423)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:57.459 [0m[32m[1650314516684584/write/3 (pid 12424)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:57.466 [0m[32m[1650314516684584/write/4 (pid 12425)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:57.473 [0m[32m[1650314516684584/write/5 (pid 12426)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:57.481 [0m[32m[1650314516684584/write/6 (pid 12427)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:58.438 [0m[32m[1650314516684584/write/3 (pid 12424)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:58.450 [0m[32m[1650314516684584/read/7 (pid 12438)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:58.452 [0m[32m[1650314516684584/write/2 (pid 12423)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:58.463 [0m[32m[1650314516684584/read/8 (pid 12439)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:58.465 [0m[32m[1650314516684584/write/5 (pid 12426)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:58.473 [0m[32m[1650314516684584/read/9 (pid 12440)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:58.478 [0m[32m[1650314516684584/write/6 (pid 12427)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:58.487 [0m[32m[1650314516684584/read/10 (pid 12441)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:58.489 [0m[32m[1650314516684584/write/4 (pid 12425)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:58.496 [0m[32m[1650314516684584/read/11 (pid 12442)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:41:59.314 [0m[32m[1650314516684584/read/7 (pid 12438)] [0m[22mfile contents: this is step 1[0m
    [35m2022-04-18 13:41:59.348 [0m[32m[1650314516684584/read/8 (pid 12439)] [0m[22mfile contents: this is step 0[0m
    [35m2022-04-18 13:41:59.350 [0m[32m[1650314516684584/read/9 (pid 12440)] [0m[22mfile contents: this is step 3[0m
    [35m2022-04-18 13:41:59.362 [0m[32m[1650314516684584/read/11 (pid 12442)] [0m[22mfile contents: this is step 2[0m
    [35m2022-04-18 13:41:59.370 [0m[32m[1650314516684584/read/10 (pid 12441)] [0m[22mfile contents: this is step 4[0m
    [35m2022-04-18 13:41:59.450 [0m[32m[1650314516684584/read/7 (pid 12438)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:59.479 [0m[32m[1650314516684584/read/9 (pid 12440)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:59.482 [0m[32m[1650314516684584/read/8 (pid 12439)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:59.495 [0m[32m[1650314516684584/read/10 (pid 12441)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:59.497 [0m[32m[1650314516684584/read/11 (pid 12442)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:41:59.505 [0m[32m[1650314516684584/join/12 (pid 12459)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:42:00.183 [0m[32m[1650314516684584/join/12 (pid 12459)] [0m[22mstep numbers were: [0, 3, 2, 1, 4][0m
    [35m2022-04-18 13:42:00.261 [0m[32m[1650314516684584/join/12 (pid 12459)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:42:00.269 [0m[32m[1650314516684584/end/13 (pid 12462)] [0m[1mTask is starting.[0m
    [35m2022-04-18 13:42:01.027 [0m[32m[1650314516684584/end/13 (pid 12462)] [0m[1mTask finished successfully.[0m
    [35m2022-04-18 13:42:01.027 [0m[1mDone![0m
    [0m
