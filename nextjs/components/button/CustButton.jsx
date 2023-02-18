"use client"

import { getNewItem } from "@/pages/api/item";

export default function CustButton({color="indigo", children, onClickAction }) {

    let buttonAction = undefined

    if (onClickAction == "getNewItem") {
        buttonAction = getNewItem
    }

    const buttonStyles = {
        colors: {
        red: "bg-red-500",
        green: "bg-green-500",
        indigo: "bg-indigo-500"
        }
    }

    return (
        <button type="button" onClick={buttonAction} className={`rounded-lg ${buttonStyles.colors[color]}`}>{children}</button>
    );
};