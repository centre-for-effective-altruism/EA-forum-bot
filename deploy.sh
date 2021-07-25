#!bin/bash
gcloud functions deploy ea-forum-posts \
    --project=ea-forum-posts \
    --trigger-topic ea-forum-post \
    --memory=256MB \
    --env-vars-file .env.yaml \
    --region=us-central1 \
    --runtime python39 \
    --entry-point=post_tweet