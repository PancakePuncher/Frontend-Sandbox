"use client"

import type { NextPage } from 'next'
import React from 'react';
import Head from 'next/head'
import { useQuery, gql } from '@apollo/client';

const query = gql`
    query {
        item {
            id
            name
            icon64
            iconUrl
            desc
        }
  }
`;

const Home: NextPage = () => {

  const { loading, error, data, refetch } = useQuery(query, {
    context: {uri: "https://code.pancakepuncher.com/proxy/8000/item"}
  });

  const itemCard = () => {
    if (data) {
        return (
          <div className="grid h-96 w-96 mt-10 bg-gray-700 place-content-center rounded-lg border"> 
            <h1 className="place-self-center mt-2">{data.item.id + " : " + data.item.name}</h1>
            <img className="place-self-center h-60" src={data.item.icon64} alt={data.item.iconUrl} />
            <h2 className="place-self-center h-24 w-96 text-center p-8">{data.item.desc}</h2>
          </div>
      )
    }

    if (loading) {
      return (
        <div className="grid h-96 w-96 mt-10 bg-gray-700 place-content-center rounded-lg border"> 
          <h1 className="place-self-center">Retrieving Item</h1>
        </div>
      )
    }

    if (error) {
      return (
        <div className="grid h-96 w-96 mt-10 bg-gray-700 place-content-center rounded-lg border"> 
          <h1 className="place-self-center">Error Retrieving Item</h1>
        </div>
      )
    }

    return <div>Something Serious went wrong...</div>
  }

  return (
      <div>
        <Head>
          <title>OSRS Item Quiz</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <main>
          <div className="grid gap-2 place-content-center pt-50 h-96">
            {itemCard()}
          </div>
          <div className="grid gap-2 place-content-center pt-10">
            <div className="grid grid-cols-2 place-content-center gap-5">
              <button className="bg-green-500 my-2 p-2 px-5 rounded-lg">True</button>
              <button className="bg-red-500 my-2 p-2 px-5 rounded-lg">False</button>
            </div>
            <div className="grid grid-cols-1 place-content-center">
              <button onClick={() => refetch()} className="bg-indigo-500 p-2 px-5 rounded-lg">New Item</button>
            </div>
          </div>
        </main>

        <footer>
          <div className="absolute bottom-0 right-0 mb-5 mr-5 text-gray-600 text-xs">Made by PancakePuncher c:</div>
        </footer>
      </div>
    )
}

export default Home
