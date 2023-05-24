#!bin/bash
gcloud scheduler jobs create pubsub ea-forum-post \
    --project=ea-forum-posts-387615 \
    --schedule="30 6-21/3 * * *" \
    --topic=ea-forum-post \
    --location=us-central1 \
    --description="Post a top post from the EA Forum" \
    --message-body="Post a top post from the EA Forum"