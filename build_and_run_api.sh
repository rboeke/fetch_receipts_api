docker build -t receipts_api .
echo ""
echo "Receipts API has the following CONTAINER ID: "
docker run -d -p 5000:5000 receipts_api:latest
echo ""
echo "Receipts API is now running at 0.0.0.0:5000"
echo ""
echo "To stop, run docker stop <container_id listed above>"