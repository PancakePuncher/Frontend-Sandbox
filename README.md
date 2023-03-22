# Table of Contents
- [What is this app?](#what-is-this-app)
- [Can I fork or use this app?](#can-i-fork-or-use-this-app)
- [What is this built on?](#what-is-this-built-on)

____

## What is this app?

This is a small project I created to test and improve upon my web development skills. The goal of this application is to demonstrate implementation and use of modern programming technologies best to my ability.

As it stands this application allows end users to provide "True" or "False" responses to questions pertaining to items from the popular MMORPG called "Old School Runescape" often abbreviated as OSRS or 07 Scape.

Through the use of this app I aim to try and create a more comprehensive and complete understanding of the current items in OSRS to build interesting data sets due to my own personal interest.

_____

## Can I fork or use this app?

As it stands this application is licensed under the MIT License. Please refer to it if you wish to fork or us this application in any way.

As it stands the only thing not provided in this source code is the items database I created by scraping OSRS's public API.

_____

## What is this built on?

As it stands this application utilizes the below libraries:

- Frontend
    - TypeScript
        - NextJS
        - GraphQL
        - Apollo
        - Tailwinds CSS
- Backend
    - Python
        - FastAPI
        - Strawberry
        - Asyncio
        - Peewee
- Database
    - SQLite

In more detail:

This application is build on NextJS/ReactJS and utilizes GraphQL and Apollo Client to send API request to FastAPI. FastAPI uses Strawberry to ingest and process GraphQL request. Data is stored in a SQLite Database. All processes are currently asynchronous.
