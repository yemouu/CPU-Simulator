# cpu-simulator
KSU Operating Systems Project 2

# Running
If you are using Nix/NixOS this project can be run with:
```sh
nix run
```

In other environments, install [hatch](https://hatch.pypa.io/latest/install/) and run the command:
```sh
hatch run cpu-schedulers
```

# Modifying the Simulation
As of right now, there currently isn't any GUI or REPL so in order to modify which scheduler is being used, the
processes in the system, the tasks each process has, the resource manager and the number of resources in the system,
you will need to edit the `main()` function in `cpu_schedulers/__main__.py` directly.

To begin with, you can define a resource manager:
```py
resource_manager = ResourceManager((Resource(),))
```

NOTE: The resource manager requires a tuple of resources so if you want only one resource you need to specify
`(Resource(),)`.

There are currently three resource managers:
- `ResourceManager` - Generic resource manager that gives a process access to a resource as long as its available
- `ResourceAllocationGraph` - Resource manager that can detect deadlocks
- `AvoidantResourceAllocationGraph` - Resource manager that can detect and avoid deadlocks

Next you can define your list of processes:
```py
processes = [
    Process(0, 5, []),
    Process(
        0,
        2,
        [
            Task(TaskAction.RESOURCE_REQUEST, 0),
            Task(TaskAction.YIELD, 1),
        ],
    ),
]
```

A process object is created with its arrival time into the system, how many processing ticks the process will have, and
the tasks that a process will have.
The first process in this list arrives at tick 0, will have 5 processing ticks, and has no tasks.
The second process in this list also arrives at tick 0, but will have 2 processing ticks, and has two tasks.
One of these tasks is to request resource 0, and the other task is to yield for 1 second.

The available tasks are:
- `NONE` - Do nothing and take a processing tick
- `RESOURCE_RELEASE` - Release a resource
- `RESOURCE_REQUEST` - Request a resource
- `YIELD` - Yield execution

Finally you can choose the scheduler you want to use.
There are currently two implemented schedulers, `FirstComeFirstServe` and `RoundRobin`.

```py
scheduler = FirstComeFirstServe(processes, resource_manager)
# To use round robin with a time quantum of 2:
# scheduler = RoundRobin(processes, resource_manager, 2)
```

All together this would look like the following inside the `main()` function of `cpu_schedulers/__main__.py`:

```py
resource_manager = ResourceManager((Resource(),))
processes = [
    Process(0, 5, []),
    Process(
        0,
        2,
        [
            Task(TaskAction.RESOURCE_REQUEST, 0),
            Task(TaskAction.YIELD, 1),
        ],
    ),
]

scheduler = FirstComeFirstServe(processes, resource_manager)
# To use round robin with a time quantum of 2:
# scheduler = RoundRobin(processes, resource_manager, 2)
```

# License
This project is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/).
