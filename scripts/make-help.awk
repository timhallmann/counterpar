#!/usr/bin/awk -f

# Script for 'make help' functionality.

# Prints targets and their notes, e.g.:
# #@ Note1
# #@ Note2
# target: dependencies
#     rules
#
# , which will be printed as:
# target  Note1
#         Note2
#
# .

# Note that this script doesn't handle every valid target name correct, e.g.
# when the target name contains a (masked) ':'.
#
# Note further that this script was developed with gawk, I did not check for
# compatibility with other implementations (should be pretty standard though).

# Inspired by:
#  https://le-gall.bzh/post/makefile-based-ci-chain-for-go/
#  https://medium.com/@exustash/three-good-practices-for-better-ci-cd-makefiles-5b93452e4cc3

# Copyright (c) 2020 Tim Hallmann <tim@t8w.de>
# License: MIT

BEGIN {
    ORS = "" # No newline separator between prints.
}

/^#@/ { # Save a note.
    notes[++i] = substr($0, 4)
}

/^[^.#].+?:/ { # Save a target.
    if(targetsy[j] == i) next # Ignore targets without notes.

    targets[++j] = substr($0, 0, index($0, ":") - 1)

    # Save longest targets' length.
    l = length(targets[j])
    if(max < l) max = l

    # Save a reference where this targets notes end.
    targetsy[j] = i
}

{
    # Save a single extra newline if there are 2 or more newlines following
    # each other.
    if($0 != "") {
        k = 0
        next
    }
    ++k
    if(k == 2) {
        newline[j] = "\n"
        k = 0
        next
    }
}

END {
    max += 2
    for (i = 1; i <= j; ++i) { # For each target:
        # Print the target (in blue) with its first note and the minimal required
        # padding for the longest target.
        printf "\033[36m%*-s\033[0m%s\n", max, targets[i], notes[targetsy[i-1] + 1]

        # Print all other notes, if any.
        for(k = targetsy[i-1] + 2; k <= targetsy[i]; ++k)
            printf "%*-s%s\n", max, "", notes[k]

        # Print an extra newline, if set.
        print newline[i]
    }
}
