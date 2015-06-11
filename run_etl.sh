echo "Setting up MongoDB"
mongod

echo "Running ETL"
cd preprocessor
python preprocessor.py