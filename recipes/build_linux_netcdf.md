# How to build SWAN on Linux with netCDF support

## Prerequisites

### On your laptop/desktop PC
You should have a regular, non-root user with sudo privileges in order to install new packages.

### On a computer cluster
Users at clusters usually have no admin/root access, but some compilers are already installed. If no compilers are available in your system, try to [install gfortran in Linux as a user](https://stackoverflow.com/questions/35274894/installing-gfortran-in-linux-as-a-user).

I checked if the GNU Fortran compiler was in my system by typing `gfortran --version`:
```bash
   GNU Fortran (GCC) 4.8.5 20150623 (Red Hat 4.8.5-36)
```
And then for the Intel® Fortran compiler I called the `ifort -V` command:
```bash
   Intel(R) Fortran Intel(R) 64 Compiler XE for applications running on Intel(R) 64, Version 14.0.0.080 Build 20130728
```
So I have two choices. It is mandatory to set one of them as the default compiler, using the `export FC=` command.

If you go for the GNU compiler, type:
```bash
export FC=gfortran
```
Or maybe you prefer the Intel® one. Just:
```bash
export FC=ifort
```
Now, **skip to step 2**.


## Step 1. Install compilers and building tools
First let's check which Linux are you running with the command:
```bash
lsb_release -ds
```
Will return something like:
```bash
   Debian GNU/Linux 9.8 (stretch)
```
```bash
   CentOS Linux release 7.6.1810 (Core)
```
SWAN is a program written in Fortran, so we're going to install the GNU Fortran compiler and some building tools as they are Open Source.

* For *Debian/Ubuntu/Linux Mint*:
```bash
sudo apt-get update
sudo apt-get install wget nano gfortran m4 build-essential
```
* For *Red Hat/Fedora/Mandriva/CentOS*:
```bash
sudo yum install wget nano gcc-gfortran m4
sudo yum groupinstall 'Development Tools'
```
* For *Archlinux/Manjaro*:
```bash
sudo pacman -Sy wget base-devel gcc-fortran
```
After installing, we need to set the GNU Fortran compiler as the default compiler:
```bash
export FC=gfortran
```


## Step 2. Install netCDF
Until version 4.1.3, `netCDF` was bundled in a single package. Since then, has been split off into independent distributions (`netCDF-C`, `netCDF-Fortran`, `netCDF-Java`, `netCDF-Python`, `netCDF-C++` and so on).

For SWAN, we only need `netCDF-Fortran`, but it depends on the “parent” `netCDF-C`, so we will install both.

Let's start with downloading and installing `netCDF-C` in a new folder called `netcdf` in user home directory (e.g. `/home/james/`):
```bash
wget https://github.com/Unidata/netcdf-c/archive/v4.6.3.tar.gz
tar -xzf v4.6.3.tar.gz
cd netcdf-c-4.6.3
./configure --prefix=${HOME}/netcdf --disable-dap --disable-netcdf-4 --disable-shared
make
make install
cd ${HOME}
```
Then we'll do the same with `netCDF-Fortran`, in a new folder called `netcdf-fortran`:
```bash
wget https://github.com/Unidata/netcdf-fortran/archive/v4.4.5.tar.gz
tar -xzf v4.4.5.tar.gz
cd netcdf-fortran-4.4.5
CPPFLAGS="-I${HOME}/netcdf/include" LDFLAGS="-L${HOME}/netcdf/lib" LD_LIBRARY_PATH="${HOME}/netcdf/lib" LIBS="-lnetcdf -lhdf5_hl -lhdf5 -lz -lcurl" ./configure --disable-shared --prefix=${HOME}/netcdf-fortran
make
make install
cd ${HOME}
```
Once installed, let's tell the system where to find our new libraries:
```bash
export PATH="${HOME}/netcdf/bin:${HOME}/netcdf-fortran/bin:$PATH"
export LD_LIBRARY_PATH="${HOME}/netcdf/lib:${HOME}/netcdf-fortran/lib:${LD_LIBRARY_PATH}"
```
Enter this command to view details about our new libraries:
```bash
nf-config --all
```
It should look like this:
```bash
This netCDF-Fortran 4.4.6-development has been built with the following features:
  --cc        -> icc
  --cflags    ->  -I/home/james/netcdf-fortran/include -I/home/james/netcdf/include
  --fc        -> ifort
  --fflags    -> -I/home/james/netcdf-fortran/include
  --flibs     -> -L/home/james/netcdf-fortran/lib -lnetcdff -L/home/james/netcdf/lib -lnetcdf -lsz -lcurl -lm -lnetcdf -lhdf5_hl -lhdf5 -lz -lcurl
  --has-f90   -> no
  --has-f03   -> yes
  --has-nc2   -> yes
  --has-nc4   -> no
  --prefix    -> /home/james/netcdf-fortran
  --includedir-> /home/james/netcdf-fortran/include
  --version   -> netCDF-Fortran 4.4.6-development
```
Open a text editor and copy `--fflags`, `--flibs` and `--prefix` lines. We will need that info to build SWAN later.


## Step 3. Download source code
Use `wget` command to download SWAN:
```bash
wget https://github.com/javirg/SWAN-Support/raw/master/source/swan4120.tar.gz
```
We need to extract the files before building. Most common procedure is to use the `tar` command with `-x`, `-z` and `-f` filters, as we did previously with netCDF packages:
```bash
tar -xzf swan4120.tar.gz
```
Now all files were extracted to a new folder called `swan4120`. Let's dig into it:
```bash
cd swan4120
```


## Step 4. Build
Here's the point where the procedure diverges depending on which mode do you want to run SWAN:

* **Serial**: for computers only using one processor (like your PC)
* **Parallel, shared (OMP)**: for shared memory systems (like your PC, using multiple processors)
* **Parallel, distributed (MPI)**: for distributed memory systems (like clusters)

**Follow just one of the following (A, B or C) instructions!**

### A - Serial mode
Configure SWAN for Unix systems and NetCDF by executing the `switch.pl` Perl script:
```bash
perl switch.pl -unix -netcdf
```
Next, generate a config file based on your system:
```bash
make config
```
Let's edit the `macros.inc` file with `nano` editor:
```bash
nano macros.inc
```
We need to:
* Set `FLAGS_SER` to the `--fflags` we'd seen before.
* Set `NETCDFROOT` to the `--prefix` we'd seen before.
* Set `LIBS_SER` to the `--flibs` we'd seen before.

Note: Instead of `/home/username/`, you can type `${HOME}` as shortcut. After editing, `macros.inc` should look like this:
```bash
##############################################################################
# IA32_Intel/x86-64_Intel:      Intel Pentium with Linux using Intel compiler 17.
##############################################################################
F90_SER = ifort
F90_OMP = ifort
F90_MPI = mpiifort
FLAGS_OPT = -O2
FLAGS_MSC = -W0 -assume byterecl -traceback -diag-disable 8290 -diag-disable 8291 -diag-disabl$
FLAGS90_MSC = $(FLAGS_MSC)
FLAGS_DYN = -fPIC
FLAGS_SER = -I${HOME}/netcdf-fortran/include
FLAGS_OMP = -qopenmp
FLAGS_MPI =
NETCDFROOT = ${HOME}/netcdf-fortran
ifneq ($(NETCDFROOT),)
  INCS_SER = -I$(NETCDFROOT)/include
  INCS_OMP = -I$(NETCDFROOT)/include
  INCS_MPI = -I$(NETCDFROOT)/include
  LIBS_SER = -L${HOME}/netcdf-fortran/lib -lnetcdff -L${HOME}/netcdf/lib -lnetcdf -lsz -lcurl -lm -lnetcdf -lhdf5_hl -lhdf5 -lz -lcurl
  LIBS_OMP = -L$(NETCDFROOT)/lib -lnetcdf -lnetcdff
  LIBS_MPI = -L$(NETCDFROOT)/lib -lnetcdf -lnetcdff
  NCF_OBJS = nctablemd.o agioncmd.o swn_outnc.o
else
...blablabla...
```
Ready to build SWAN. To do it in parallel-distributed mode, type:
```bash
make ser
```
**Go to step 5**

### B - Parallel, shared mode (OMP)
Configure SWAN for Unix systems and NetCDF by executing the `switch.pl` Perl script:
```bash
perl switch.pl -unix -netcdf
```
Next, generate a config file based on your system:
```bash
make config
```
Let's edit the `macros.inc` file with `nano` editor:
```bash
nano macros.inc
```
We need to:
* Set `FLAGS_OMP` to the `--fflags` we'd seen before. **Don't delete `-qopenmp` or any previous line content!**
* Set `NETCDFROOT` to the `--prefix` we'd seen before.
* Set `LIBS_OMP` to the `--flibs` we'd seen before.

Note: Instead of `/home/username/`, you can type `${HOME}` as shortcut. After editing, `macros.inc` should look like this:
```bash
##############################################################################
# IA32_Intel/x86-64_Intel:      Intel Pentium with Linux using Intel compiler 17.
##############################################################################
F90_SER = ifort
F90_OMP = ifort
F90_MPI = mpiifort
FLAGS_OPT = -O2
FLAGS_MSC = -W0 -assume byterecl -traceback -diag-disable 8290 -diag-disable 8291 -diag-disabl$
FLAGS90_MSC = $(FLAGS_MSC)
FLAGS_DYN = -fPIC
FLAGS_SER =
FLAGS_OMP = -qopenmp -I${HOME}/netcdf-fortran/include
FLAGS_MPI =
NETCDFROOT = ${HOME}/netcdf-fortran
ifneq ($(NETCDFROOT),)
  INCS_SER = -I$(NETCDFROOT)/include
  INCS_OMP = -I$(NETCDFROOT)/include
  INCS_MPI = -I$(NETCDFROOT)/include
  LIBS_SER = -L$(NETCDFROOT)/lib -lnetcdf -lnetcdff
  LIBS_OMP = -L${HOME}/netcdf-fortran/lib -lnetcdff -L${HOME}/netcdf/lib -lnetcdf -lsz -lcurl -lm -lnetcdf -lhdf5_hl -lhdf5 -lz -lcurl
  LIBS_MPI = -L$(NETCDFROOT)/lib -lnetcdf -lnetcdff
  NCF_OBJS = nctablemd.o agioncmd.o swn_outnc.o
else
...blablabla...
```
Ready to build SWAN. To do it in parallel-distributed mode, type:
```bash
make omp
```
**Go to step 5**

### C - Parallel, distributed mode (MPI)
Configure SWAN for Unix systems, NetCDF and MPI by executing the `switch.pl` Perl script:
```bash
perl switch.pl -unix -netcdf -mpi
```
Next, generate a config file based on your system:
```bash
make config
```
Let's edit the `macros.inc` file with `nano` editor:
```bash
nano macros.inc
```
We need to:
* If using Intel® Fortran compilers, set `F90_MPI` to `mpiifort`.
* Set `FLAGS_MPI` to the `--fflags` we'd seen before.
* Set `NETCDFROOT` to the `--prefix` we'd seen before.
* Set `LIBS_MPI` to the `--flibs` we'd seen before.

Note: Instead of `/home/username/`, you can type `${HOME}` as shortcut. After editing, `macros.inc` should look like this:
```bash
##############################################################################
# IA32_Intel/x86-64_Intel:      Intel Pentium with Linux using Intel compiler 17.
##############################################################################
F90_SER = ifort
F90_OMP = ifort
F90_MPI = mpiifort
FLAGS_OPT = -O2
FLAGS_MSC = -W0 -assume byterecl -traceback -diag-disable 8290 -diag-disable 8291 -diag-disabl$
FLAGS90_MSC = $(FLAGS_MSC)
FLAGS_DYN = -fPIC
FLAGS_SER =
FLAGS_OMP = -qopenmp
FLAGS_MPI = -I${HOME}/netcdf-fortran/include
NETCDFROOT = ${HOME}/netcdf-fortran
ifneq ($(NETCDFROOT),)
  INCS_SER = -I$(NETCDFROOT)/include
  INCS_OMP = -I$(NETCDFROOT)/include
  INCS_MPI = -I$(NETCDFROOT)/include
  LIBS_SER = -L$(NETCDFROOT)/lib -lnetcdf -lnetcdff
  LIBS_OMP = -L$(NETCDFROOT)/lib -lnetcdf -lnetcdff
  LIBS_MPI = -L${HOME}/netcdf-fortran/lib -lnetcdff -L${HOME}/netcdf/lib -lnetcdf -lsz -lcurl -lm -lnetcdf -lhdf5_hl -lhdf5 -lz -lcurl
  NCF_OBJS = nctablemd.o agioncmd.o swn_outnc.o
else
...blablabla...
```
Ready to build SWAN. To do it in parallel-distributed mode, type:
```bash
make mpi
```
**Go to step 5**


## Step 5. Finish
If no errors were shown during the building process, we've successfully built SWAN.

The built files need executable permissions. Let's fix them with `chmod +x` command:
```bash
chmod +x swanrun swan.exe
```
I like to have those files on my HOME folder (e.g. `/home/james`). Copy them with `cp` and move to it by `cd`:
```bash
cp -r 'swan.exe' 'swanrun' ${HOME}
cd ${HOME}
```
Once SWAN is built, we don't need the source files anymore. Clean up both the `.tar.gz` files and the `swan4120`, `netcdf-c-4.6.3` and `netcdf-fortran-4.4.5` folders:
```bash
rm -rf *.tar.gz swan4120 netcdf-c-4.6.3 netcdf-fortran-4.4.5
```
That's it. Now, you can run SWAN by calling `swanrun -input [filename]`.