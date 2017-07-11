# SSL terminated containers on rancher

1. Launch the service
2. Update the LB, add 80/443 routes to point to the service.
3. Wait until route53 container has synced the entry to AWS
4. Once that's done, `make export; git add -p` and overwrite the DNS entry
   instead as a CNAME to lb.lb.galaxians.org (like all the others). Do not
   allow it to add the other changes, it will result in annoying errors.
5. Now we can update letsencrypt, add new DNS entry. Should be done here.
