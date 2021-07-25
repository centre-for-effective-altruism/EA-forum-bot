#!bin/bash
gcloud scheduler jobs create pubsub ea-forum-post \
    --project=ea-forum-posts \
    --schedule="0 6-21/3 * * *" \
    --topic=ea-forum-post \
    --description="Post a top post from the EA Forum" \
    --message-body="Post a top post from the EA Forum"