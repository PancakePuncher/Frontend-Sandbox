"use client";

import type { NextPage } from "next";
import React from "react";
import Head from "next/head";
import { useQuery, gql } from "@apollo/client";

const getItemInfo = gql`
    query {
        randitem {
            id
            name
            desc
            icon64
        }
        randQuestion {
            question
        }
    }
`;

const Home: NextPage = () => {
    const { loading, error, data, refetch } = useQuery(getItemInfo, {
        context: { uri: "https://code.pancakepuncher.com/proxy/8000/item" },
    });

    const itemCard = () => {
        if (data) {
            return (
                <div>
                    <div className="grid h-96 w-96 mt-36 bg-gray-700 place-content-center rounded-lg border">
                        <h1 className="place-self-center mt-2">
                            {data.randitem.id + " : " + data.randitem.name}
                        </h1>
                        <img
                            className="place-self-center h-60"
                            src={data.randitem.icon64}
                            alt=""
                        />
                        <h2 className="place-self-center h-24 w-96 text-center p-8">
                            {data.randitem.desc}
                        </h2>
                    </div>
                    <div className="grid place-content-center mt-4 mb-4 p-4 bg-gray-700 rounded-lg border">
                        <p>{data.randQuestion.question}</p>
                    </div>
                </div>
            );
        }

        if (loading) {
            return (
                <div className="grid h-96 w-96 mt-10 bg-gray-700 place-content-center rounded-lg border">
                    <h1 className="place-self-center">Retrieving Item</h1>
                </div>
            );
        }

        if (error) {
            return (
                <div className="grid h-96 w-96 mt-10 bg-gray-700 place-content-center rounded-lg border">
                    <h1 className="place-self-center">Error Retrieving Item</h1>
                </div>
            );
        }

        return <div>Something Serious went wrong...</div>;
    };

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
                <div className="grid gap-2 place-content-center mt-28">
                    <div className="grid grid-cols-2 place-content-center gap-5">
                        <button className="bg-green-500 my-2 p-2 px-5 rounded-lg">
                            True
                        </button>
                        <button className="bg-red-500 my-2 p-2 px-5 rounded-lg">
                            False
                        </button>
                    </div>
                    <div className="grid grid-cols-1 place-content-center">
                        <button
                            onClick={() => refetch()}
                            className="bg-indigo-500 p-2 px-5 rounded-lg"
                        >
                            New Item
                        </button>
                    </div>
                </div>
            </main>

            <footer>
                <div className="absolute bottom-0 right-0 mb-5 mr-5 text-gray-600 text-xs">
                    Made by PancakePuncher c:
                </div>
            </footer>
        </div>
    );
};

export default Home;
