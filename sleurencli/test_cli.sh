#!/bin/bash
#
################################################################################
##                          Test Sleuren CLI                                  ##
################################################################################

LOG_FILE="sleuren.log"
NOW=$(date +'%Y-%m-%d %a %T')

# Function to test a CLI call
# Parameters: 1 command
function test
{
    echo "$1"
    echo "$1" >> "$LOG_FILE"
    $1 >> "$LOG_FILE"

    # check if result contains "Traceback" and exit if it does
    LINE=$(grep -m 1 "Traceback" "$LOG_FILE")
    if [[ -n "$LINE" ]]; then
        echo
        echo "-------------------------------------"
        echo " Test failed for $1"
        echo "-------------------------------------"
        exit 1
    fi

    # check if result contains "ERROR:" and exit if it does
    LINE=$(grep -m 1 "ERROR:" "$LOG_FILE")
    if [[ -n "$LINE" ]]; then
        echo
        echo "-------------------------------------"
        echo " Test failed for $1"
        echo "-------------------------------------"
        exit 1
    fi

    # check if result contains "Failed" and exit if it does
    LINE=$(grep -m 1 "Failed" "$LOG_FILE")
    if [[ -n "$LINE" ]]; then
        echo
        echo "-------------------------------------"
        echo " Test failed for $1"
        echo "-------------------------------------"
        exit 1
    fi
}

if [[ -n $1 ]]; then
    CMD="$1"
else
    CMD="./sleurencli.py"
fi

echo "--- Test $NOW ---" > "$LOG_FILE"

test "$CMD"
test "$CMD --version"
test "$CMD config"
test "$CMD config --help"
test "$CMD config print"
test "$CMD config save"
test "$CMD servers"
test "$CMD servers add"
test "$CMD servers list"
test "$CMD servers remove"
test "$CMD sites"
test "$CMD sites add --url sleuren.com"
test "$CMD sites list"
test "$CMD sites list --help"
test "$CMD sites list --csv"
test "$CMD statistics"
test "$CMD tokens"
test "$CMD tokens list"
test "$CMD tokens list --csv"

sleep 10

test "$CMD sites list --url sleuren.com"
test "$CMD sites remove --url sleuren.com"

echo
echo "-------------------------------------"
echo " Test successfully"
echo "-------------------------------------"
