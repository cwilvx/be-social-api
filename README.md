# B-social backend
(Work in progress) an educational social network for my campus. This repo hosts the Flask APIs serving the Be Social App

### Settting up locally

```bash
# for ssh users
$ git clone git@github.com:geoffrey45/be-social-be.git 
# for HTTPS users
$ git clone https://github.com/geoffrey45/be-social-be.git
$ cd be-social-be
# install dependencies
$ pipenv shell
$ pipenv install --dev
$ chmod a+x start.sh
# rename start.sh.example to start.sh and edit the configs
$ ./start.sh
```

### The endpoints
> For Authorization, the `access_token` is sent as a bearer token.

| Endpoint      | Type |                  Parameters                  | Authorization | Returns                                                                |
|---------------|------|:--------------------------------------------:|:-------------:|------------------------------------------------------------------------|
| /api/register | POST | `username: string`<br><br>`password: string` |       No      | `201 Created`                                                          |
| /api/login    | POST | `username: string`<br><br>`password: string` |       No      | `200 OK`<br><br>`acccess_token: string`<br><br>`refresh_token: string` |
| /posts        | GET  |                      N/A                     |       No      | A list of posts                                                        |
| /posts/new    | POST |   Authorization<br><br>`post_body: string`   |      Yes      | `201 Created`                                                          |

