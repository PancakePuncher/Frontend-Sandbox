"use client";

import type { NextPage } from "next";
import React, { useState } from "react";
import Head from "next/head";
import { useQuery, gql, useMutation } from "@apollo/client";

const getPageDetails = gql`
    query {
        PageDetails {
            itemId
            itemName
            itemDesc
            itemIcon64
            questionId
            questionText
            truthyValue
            falsyValue
        }
    }
`;

const sendAnswer = gql`
    mutation receiveUserAnswer($answer: Int!, $questionId: Int!, $itemId: Int!) {
        receiveUserAnswer(answer: $answer, questionId: $questionId, itemId: $itemId)
    }
`;

const Home: NextPage = () => {

    const [buttonState, setButtonState] = useState(false)

    const initQuery = useQuery(getPageDetails, {
        context: { uri: "https://code.pancakepuncher.com/proxy/8000/graphql" },
    });

    const [userAnswerGraphQLMutation] = useMutation(sendAnswer, {
        context: { uri: "https://code.pancakepuncher.com/proxy/8000/graphql" },
    });

    function buttonStateFlipper() {
        setButtonState(true)
        setTimeout(() => setButtonState(false), 500)
    }

    const onTrueFalseClick = (e: React.MouseEvent<HTMLButtonElement>, buttonName: number) => {

        const payload = {
                variables: {
                answer: buttonName,
                questionId: initQuery.data.PageDetails.questionId,
                itemId: initQuery.data.PageDetails.itemId
            }
        }

        userAnswerGraphQLMutation(payload)
        initQuery.refetch()
    }

    const itemCard = () => {
        if (initQuery.data) {
            return (
                <div>
                    <div className="grid h-96 w-96 mt-36 bg-gray-700 place-content-center rounded-lg border">
                        <h1 className="place-self-center mt-2">
                            {initQuery.data.PageDetails.itemId + " : " + initQuery.data.PageDetails.itemName}
                        </h1>
                        <img
                            className="place-self-center h-60"
                            src={initQuery.data.PageDetails.itemIcon64}
                            alt=""
                        />
                        <h2 className="place-self-center h-24 w-96 text-center p-8">
                            {initQuery.data.PageDetails.itemDesc}
                        </h2>
                    </div>
                    <div className="grid place-content-center mt-4 mb-4 p-4 bg-gray-700 rounded-lg border">
                        <p>{initQuery.data.PageDetails.questionText}</p>
                    </div>
                </div>
            );
        }

        if (initQuery.loading) {
            return (
                <div className="grid h-96 w-96 mt-10 bg-gray-700 place-content-center rounded-lg border">
                    <h1 className="place-self-center">Retrieving Item</h1>
                </div>
            );
        }

        if (initQuery.error) {
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
                        <button disabled={buttonState} onClick={(e) => {onTrueFalseClick(e, 1), buttonStateFlipper()}} className="bg-green-500 my-2 p-2 px-5 rounded-lg">
                            True
                        </button>
                        <button disabled={buttonState} onClick={(e) => {onTrueFalseClick(e, 0), buttonStateFlipper()}} className="bg-red-500 my-2 p-2 px-5 rounded-lg">
                            False
                        </button>
                    </div>
                    <div className="grid grid-cols-1 place-content-center">
                        <button
                            disabled={buttonState}
                            onClick={() => {initQuery.refetch(), buttonStateFlipper()}}
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
