# How to build SWAN on Linux

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
sudo apt-get install build-essential gfortran
```
* For *Red Hat/Fedora/Mandriva/CentOS*:
```bash
sudo yum install wget nano gcc-gfortran
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


## Step 2. Download source code
Use `wget` command to download SWAN:
```bash
wget https://github.com/javirg/SWAN-Support/raw/master/source/swan4120.tar.gz
```
We need to extract the files before building. Most common procedure is to use the `tar` command with `-x`, `-z` and `-f` filters:
```bash
tar -xzf swan4120.tar.gz
```
Now all files were extracted to a new folder called `swan4120`. Let's dig into it:
```bash
cd swan4120
```


## Step 3. Build
Here's the point where the procedure diverges depending on which mode do you want to run SWAN:

* **Serial**: for computers only using one processor (like your PC)
* **Parallel, shared (OMP)**: for shared memory systems (like your PC, using multiple processors)
* **Parallel, distributed (MPI)**: for distributed memory systems (like clusters)

**Follow just one of the following (A, B or C) instructions!**

### A - Serial mode
Configure SWAN for Unix systems by executing the `switch.pl` Perl script:
```bash
perl switch.pl -unix
```
Next, generate a config file based on your system:
```bash
make config
```
Ready to build SWAN. To do it in parallel-distributed mode, type:
```bash
make ser
```

### B - Parallel, shared mode (OMP)
Configure SWAN for Unix systems by executing the `switch.pl` Perl script:
```bash
perl switch.pl -unix
```
Next, generate a config file based on your system:
```bash
make config
```
Ready to build SWAN. To do it in parallel-distributed mode, type:
```bash
make omp
```

### C - Parallel, distributed mode (MPI)
Configure SWAN for Unix systems and MPI by executing the `switch.pl` Perl script:
```bash
perl switch.pl -unix -mpi
```
Next, generate a config file based on your system:
```bash
make config
```

If you're using Intel® Fortran compilers, you need to modify `macros.inc` file and set `mpiifort` as MPI compiler. Open the file with `nano` text editor by:
```bash
nano +6 macros.inc
```
Change `F90_MPI = mpif90` for `F90_MPI = mpiifort` on 6th line. Press `Ctrl+O`, `Enter` to Save, followed by `Ctrl+X` to close the text editor.

Ready to build SWAN. To do it in parallel-distributed mode, type:
```bash
make mpi
```


## Step 4. Finish
If no errors were shown during the building process, we've successfully built SWAN.

The built files need executable permissions. Let's fix them with `chmod +x` command:, and copy them to our home folder `cp -r` with these commands:
```bash
chmod +x swanrun swan.exe
```
I like to have those files on my HOME folder (e.g. `/home/james`). Copy them with `cp` and move to it by `cd`:
```bash
cp -r 'swan.exe' 'swanrun' ${HOME}
cd ${HOME}
```
Once SWAN is built, we don't need the source files anymore. Clean up both the `.tar.gz` file and the `swan4120` folder:
```bash
rm -rf *.tar.gz swan4120
```

That's it. Now, you can run SWAN by calling `swanrun -input [filename]`.