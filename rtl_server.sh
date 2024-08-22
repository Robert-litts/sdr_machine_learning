#!/bin/bash

# RTL-FM configuration
FREQ="105300000"         # Frequency in Hz
SAMPLE_RATE="240000"   # Sample rate
GAIN="33"               # Gain
TCP_PORT="5000"         # TCP port for netcat
ERROR_LOG="/root/error.log"  # Log file for errors

# Load configuration
#source /root/config.sh

# Function to initialize RTL-FM streaming
initialize_rtl_fm() {
  echo "Starting RTL-FM with frequency $FREQ, sample rate $SAMPLE_RATE, and gain $GAIN..."
  
  # Start rtl_fm and stream via netcat
  rtl_fm -f "$FREQ" -s "$SAMPLE_RATE" -g "$GAIN" -r 48000 2>> "$ERROR_LOG" | nc -l -p "$TCP_PORT" 2>> "$ERROR_LOG"
  
  if [ $? -ne 0 ]; then
    echo "Error: rtl_fm or netcat command failed. Check $ERROR_LOG for details." >&2
    exit 1
  fi
}

# Function to handle cleanup
cleanup() {
  echo "Cleaning up..."
  # Add any cleanup code if needed
}

# Error handling
trap 'echo "An error occurred. Check $ERROR_LOG for details." >&2; cleanup; exit 1;' ERR

# Main function
main() {
  initialize_rtl_fm
}

# Run main function
main
