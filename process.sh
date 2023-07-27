#!/bin/bash
output_dir="$1"

echo "Output directory: " "$output_dir"
mkdir -p "$output_dir"

editor_path="$(dirname $BASH_SOURCE)/editor.py"

# data_path <image-path>
function data_path {
    local file=$(basename $1)
    local path="$output_dir/${file%.*}.json"
    echo $path
}

for path in ${@:2}; do
    if [ -f "$path" ]; then
        echo $path
        data_path=$(data_path $path)
        #if [ ! -f "$data_path" ]; then
            "$editor_path" --l="$CLASS_LABELS" --data "$data_path" "$path"
            if [ $? -ne 0 ]; then exit; fi

        #else
        #    echo "Data file '$data_path' already exists, skipping"
        #fi
    fi
done
