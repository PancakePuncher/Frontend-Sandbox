"use client";

import type { NextPage } from "next";
import React from "react";
import Head from "next/head";
import { useQuery, gql, useMutation } from "@apollo/client";

const getItemInfo = gql`
    query {
        randItem {
            itemId
            itemName
            itemDesc
            itemIcon64
        }
        randQuestion {
            questionId
            questionText
        }
    }
`;

const sendAnswer = gql`
    mutation updateQuestion($answer: Int!, $questionId: Int!) {
        updateQuestion(answer: $answer, questionId: $questionId)
    }
`;

const Home: NextPage = () => {

    const itemQuery = useQuery(getItemInfo, {
        context: { uri: "https://code.pancakepuncher.com/proxy/8000/graphql" },
    });

    const [updateQuestion] = useMutation(sendAnswer, {
        context: { uri: "https://code.pancakepuncher.com/proxy/8000/graphql" },
    });

    const itemCard = () => {
        if (itemQuery.data) {
            return (
                <div>
                    <div className="grid h-96 w-96 mt-36 bg-gray-700 place-content-center rounded-lg border">
                        <h1 className="place-self-center mt-2">
                            {itemQuery.data.randItem.itemId + " : " + itemQuery.data.randItem.itemName}
                        </h1>
                        <img
                            className="place-self-center h-60"
                            src={itemQuery.data.randItem.itemIcon64}
                            alt=""
                        />
                        <h2 className="place-self-center h-24 w-96 text-center p-8">
                            {itemQuery.data.randItem.itemDesc}
                        </h2>
                    </div>
                    <div className="grid place-content-center mt-4 mb-4 p-4 bg-gray-700 rounded-lg border">
                        <p>{itemQuery.data.randQuestion.questionText}</p>
                    </div>
                </div>
            );
        }

        if (itemQuery.loading) {
            return (
                <div className="grid h-96 w-96 mt-10 bg-gray-700 place-content-center rounded-lg border">
                    <h1 className="place-self-center">Retrieving Item</h1>
                </div>
            );
        }

        if (itemQuery.error) {
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
                        <button onClick={() => {updateQuestion({ variables: {answer: 1, questionId: itemQuery.data.randQuestion.questionId}}); itemQuery.refetch()}} className="bg-green-500 my-2 p-2 px-5 rounded-lg">
                            True
                        </button>
                        <button onClick={() => {updateQuestion({ variables: {answer: 0, questionId: itemQuery.data.randQuestion.questionId}}); itemQuery.refetch();}} className="bg-red-500 my-2 p-2 px-5 rounded-lg">
                            False
                        </button>
                    </div>
                    <div className="grid grid-cols-1 place-content-center">
                        <button
                            onClick={() => itemQuery.refetch()}
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
