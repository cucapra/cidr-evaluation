# Cider Evaluation

This repository contains the evaluation materials for our ASPLOS 2023 paper
entitled "Stepwise Debugging for Hardware Accelerators".

This evaluation consists of one code artifact, the Cider Interpreter and
Interactive Debugger, and the tools required to reproduce the graphs appearing
in the paper.

**Goals**
1. To reproduce our benchmark graphs

# Setup

## Artifact Sources

This artifact is available in two formats: A docker container and through code
repositories hosted on github.

For both approaches, first clone this repository.
```
git clone https://github.com/cucapra/cidr-evaluation
```

## Docker (est. 50 min)

This requires [Docker][docker]. If running via Docker Desktop, you
will need to increase the amount of memory the containers are allowed to use via
the settings. Around 14 GB of RAM should be sufficient, less than this may cause
certain benchmarks to be killed before completing.

***Note***: running benchmarks via Docker _will_ have an impact on performance.
In particular, it can cause Verilator compilation to take notably longer than
running locally on the machine and may influence the graphs produced later.

If running on a on a system with bash:
```
bash scripts/setup.sh
```
this will build the docker image and start the container.

If running without bash, the commands can instead be invoked directly:
```
docker build . -t cider-eval:latest &&
docker run -it cider-eval:latest
```

Afterwards, you will have a terminal open in the container and can proceed to
use the artifact.

## Local Machine (est. 30-50+ min)

Running the code locally requires installing several tools:
- The Rust programming language
- Icarus Verilog
- Verilator
- Fud & the Calyx infrastructure
  - runt
- Dahlia
- (optional) TVM

The rest of this section will walk you through the process.

### Install [Rust][rust]
```bash
# On Mac and Linux
curl https://sh.rustup.rs -sSf | sh
```

### Install Rust-based tools
```bash
cargo install runt

# optional, only needed if you want to use fud's vcd-json target
cargo install vcdump
```

### Install [Verilator][verilator]
```bash
# On Mac:
brew install verilator

# On Linux
# first see https://verilator.org/guide/latest/install.html
git clone --branch v4.220 https://github.com/verilator/verilator
cd verilator && autoconf &&
./configure && make && sudo make install
```

### Install [Icarus-Verilog][icarus]
```bash
# On Mac:
brew install icarus-verilog

# On linux
git clone --branch v11_0 https://github.com/steveicarus/iverilog
sh autoconf.sh && ./configure && make && make install
```
## Steps

These are the steps listed for running the benchmarks. With each step, a link is provided with
extra information in case something goes wrong during installation. To verify `fud` stages are
installed correctly, you may also call `fud check`.

0. Install



1. Install [Calyx](https://capra.cs.cornell.edu/docs/calyx/intro.html#compiler-installation)

```bash
git clone https://github.com/cucapra/calyx.git && cargo build
```

2. Install [`fud`](https://capra.cs.cornell.edu/docs/calyx/intro.html#installing-the-command-line-driver)

```bash
pip3 install flit && flit -f fud/pyproject.toml install -s
fud config global.futil_directory <full path to Calyx repository>
```

3. Install [Verilator](https://capra.cs.cornell.edu/docs/calyx/intro.html#simulating-with-verilator) (necessary for Verilog benchmarks)

```bash
# On Mac:
brew install verilator

# On Linux
git clone https://github.com/verilator/verilator
cd verilator && git pull && git checkout master && autoconf
./configure && make && sudo make install
```

4. Install [Calyx Interpreter](https://capra.cs.cornell.edu/docs/calyx/interpreter.html#interpreting-via-fud) (necessary for interpreter benchmarks)

```bash
# From the futil repository, build in release mode.
cd interp && cargo build --release

# Additionally, add the `--no-verify` flag.
fud config stages.interpreter.flags \"--no-verify\"
```

5. Install [Icarus-Verilog](https://capra.cs.cornell.edu/docs/calyx/fud/index.html#icarus-verilog) (necessary for Icarus-Verilog benchmarks)

```bash
fud register icarus-verilog -p fud/icarus/icarus.py

# Set Verilog to high priority.
fud c stages.verilog.priority 1
```

6. Install [Dahlia frontend](https://capra.cs.cornell.edu/docs/calyx/fud/index.html#dahlia-frontend) (necessary for Polybench benchmarks)

```bash
git clone https://github.com/cucapra/dahlia.git && cd dahlia && sbt install
sbt assembly && chmod +x ./fuse

fud config stages.dahlia.exec <full path to dahlia repo>/fuse
```

7. Install [NTT](https://capra.cs.cornell.edu/docs/calyx/frontends/ntt.html#installation) (necessary for NTT benchmarks)
```bash
# From the futil repository
cd calyx-py && flit install -s && pip3 install prettytable numpy
fud register ntt -p frontends/ntt-pipeline/fud/ntt.py && fud check
```

8. Run the script

```bash
# From the futil repository
chmod u+x evaluations/cidr-pldi-2022/scripts/evaluate.sh
chmod u+x evaluations/cidr-pldi-2022/scripts/evaluate-fully-lowered.sh 
python3 evaluations/cidr-pldi-2022/process-data.py
```

This should result in 3 files in `evaluations/cidr-pldi-2022/statistics` (as well as individual run results in `/individual-results`):
- `simulation-fully-lowered-results.csv`: Simulation statistics for the interpreter after fully lowering the Calyx program. 
- `simulation-results.csv`: Simulation statistics for interpreter, Verilog, and Icarus-Verilog.
- `compilation-results.csv` Compilation statistics for Verilog and Icarus-Verilog.







[docker]: https://www.docker.com/
[rust]: https://doc.rust-lang.org/cargo/getting-started/installation.html
[verilator]: https://verilator.org/guide/latest/install.html
[icarus]: http://iverilog.icarus.com/
