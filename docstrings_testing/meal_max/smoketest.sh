#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

##########################################################
#
# Meal Management
#
##########################################################

# clear_catalog endpoint
clear_meals() {
  echo "Clearing the meals list..."
  curl -s -X DELETE "$BASE_URL/clear-meals" | grep -q '"status": "success"'
}

# add_meal endpoint
create_meal() {
  id=$1
  meal=$2
  cuisine=$3
  price=$4
  difficulty=$5

  echo "Adding meal ($id - $meal, $cuisine) to the meals list..."
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"id\":\"$id\", \"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":\"$price\", \"difficulty\":\"$difficulty\"}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Meal added successfully."
  else
    echo "Failed to add meal."
    exit 1
  fi
}

# delete_meal endpoint
delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}

# get_meal_by_id endpoint
get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    exit 1
  fi
}

# get_meal_by_name endpoint
get_meal_by_name() {
  meal=$1

  echo "Getting meal by name ($meal)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/$meal")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by name ($meal)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (name $meal):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by name ($meal)."
    exit 1
  fi
}

############################################################
#
# Battle Management
#
############################################################

# clear_combatants endpoint
clear_combatants() {
  echo "Clearing combatants..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants cleared successfully."
  else
    echo "Failed to clear combatants."
    exit 1
  fi
}

# prep_combatant endpoint
prep_combatant() {
  meal_id=$1
  meal=$2
  cuisine=$3

  echo "Adding meal to battle: $meal_id - $meal ($cuisine)..."

  response=$(curl -s -X POST "$BASE_URL/prep-combatant" \
    -H "Content-Type: application/json" \
    -d "{\"meal_id\":$meal_id, \"meal\":\"$meal\", \"cuisine\":\"$cuisine\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal prepped for battle succesfully"
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to prep meal for battle."
    exit 1
  fi
}

# get_combatants endpoint
get_combatants() {
  echo "Retrieving combatants list..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Current combatants list retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Current combatants list JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve combatants list."
    exit 1
  fi
}

# Health checks
check_health
check_db

# Clear the meals list
clear_meals

# Create meals
create_meal 1 "Ramen" "Asian" 10.0 "MED"
create_meal 2 "Fentanyl" "American" 99.0 "HIGH"
create_meal 3 "Potato" "Irish" 0.99 "LOW"
create_meal 4 "Pasta" "Italian" 14.0 "HIGH"
create_meal 5 "Cockroaches" "Alien" 5.0 "MED"

delete_meal_by_id 1
get_all_meals

get_meal_by_id 2
get_meal_by_name "Fentanyl"

clear_combatants

prep_combatant 2 "Fentanyl" "American"
prep_combatant 3 "Potato" "Irish"

get_combatants

# battle, get_leaderboard

echo "All tests passed successfully!"