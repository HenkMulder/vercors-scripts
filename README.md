VerCors scripts
---------------

Scripts to run and analyze results of the [VerCors verification tool](https://github.com/utwente-fmt/vercors).

## Prerequisites

Scripts were used in Windows using Python 3.6.2.

## Run VerCors

The run_vercors.py is the main script to run the VerCors tool. The script needs the '$VCT_HOME' path variable to determine the location of where the tool is installed.
The first argument the script needs is the path to a file with a list of (sets of) paths to examples for VerCors to run. These paths can either be absolute paths or paths relative to the '$VCT_HOME$ directory. All subsequent arguments will be passed on to VerCors, and thus need at least an option to specify which back-end needs to be used.
A call to the script could thus look as follows:
'''
python run_vercors.py example_list.txt --silicon
'''
to run all the examples that are listed in the file 'example_list.txt' with the silicon back-end.
The option '--progress' is implicitely added by the script such that VerCors outputs the information that is needed to produce the results. Also additional options specified in the input file are added automatically.

### Intermediate result files

The 'run_vercors.py' script prints the results for the runs in a comma separated values structure.
The first line contains the options that were passed on to VerCors.
The second line contains the column headers for the values in the subsequent lines. Namely
* File: The file(s) that were verified.
* Verdict. The verdict VerCors gave (e.g. Pass, Fail, Error or None in case no verdict was produced).
* Total time. The total verification time as reported by VerCors.
* Back-end time. The time that was spent in the back-end verifier.
* Parse time. The time spent in the parsing phase.

The output of the 'run_vercors.py' script can be stored in a text file which can then be analyzed with the other scripts.

## Analysis and comparison

The results produced with the 'run_vercors.py' script can be analyzed with the 'analyze_results.py' script. This script gathers the results per file and calculates for each result the mean value and the standard deviation.
The script needs one argument, namely the path to the file that contains the results to analyze.

The 'compare_results.py' script can be used to compare one or more result files. It uses functionality from the 'analyze_results.py' script to calculate mean values and standard deviations.
If the script is called with one result file the mean total verification time for each file will be printed, in descending order.
If the script is called with more than one result file, it will take the union of all the files. For each result-file it will print the mean total verification time, or -1 if there was no result or a failing result for that file. The results will be sorted descending for the relative difference in mean total verification time between the first and the last input file.
Additionally the script will print the relative difference between mean verification times for the example for the first and the last file, and wich of the input files was the quickest, per example and overall.
