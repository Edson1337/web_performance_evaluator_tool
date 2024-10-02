#!/bin/bash

# Arguments
project_name="$1"
evaluation_type="$2"

# Base directory where projects are stored
script_dir="$(dirname "$0")"
projects_dir="$script_dir/../../projects"

# Create project directory
mkdir -p "$projects_dir/$project_name"
cd "$projects_dir/$project_name" || exit 1

if [ "$evaluation_type" == "rendering" ]; then
    ssr_repo_link="$3"
    csr_repo_link="$4"

    # Clone SSR repository
    git clone "$ssr_repo_link" "${project_name}-ssr"

    # Clone CSR repository
    git clone "$csr_repo_link" "${project_name}-csr"

elif [ "$evaluation_type" == "commit" ]; then
    repository_link="$3"
    before_hash="$4"
    after_hash="$5"

    # Clone repository for 'before' version
    git clone "$repository_link" "${project_name}_before"
    cd "${project_name}_before" || exit 1
    git checkout "$before_hash"
    cd ..

    # Clone repository for 'after' version
    git clone "$repository_link" "${project_name}_after"
    cd "${project_name}_after" || exit 1
    git checkout "$after_hash"
    cd ..

else
    echo "Invalid evaluation_type: $evaluation_type" >&2
    exit 1
fi