#!/bin/sh

RANDOM_STRING=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)

#add a post with random string to the timeline
curl -X POST http://localhost:5000/api/timeline_post -d "name=anreet&email=anreet@gmail.com&content=$RANDOM_STRING"

if [ $? == 0 ]; then
    echo "data has been added succesfully!"

    #show all the timeline posts
    echo $(curl --request GET http://localhost:5000/api/timeline_post)
fi

echo "cleaning up recently made post...."

#delete the recently made post by the given user
DELETE_POST=$(curl -X POST http://localhost:5000/api/delete_timeline_post -d "name=anreet&email=anreet@gmail.com")
echo "$DELETE_POST"
