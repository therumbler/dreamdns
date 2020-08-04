#!/bin/bash

encoded_api_key=`printf $DREAMHOST_API_KEY | base64`
echo $encoded_api_key

template=`cat "k8s/deploy.yaml.template" | sed "s/{{DREAMHOST_API_KEY}}/$encoded_api_key/g"`

# apply the yaml with the substituted value
echo "$template" | kubectl apply -f -