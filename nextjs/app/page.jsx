"use client"

import CustButton from "@/components/button/CustButton";
import React, { useState, useEffect } from "react";

export default function Home() {

  const [itemData, setItemData] = useState({})

  const getNewItem = () => {
    const res = fetch("http://127.0.0.1:8000/new_item", {
        method: "GET",
      }).then(res => {
          return res.json()
      }).then(data => {
          setItemData(data.ItemData[0])
      })
  }

  useEffect(() =>
    {
      getNewItem();
    }, []
  )

  return (
    <main>
      <div className="grid gap-2 place-content-center pt-60 h-96">
        <div className="grid place-content-center w-96 h-76">        
          <h1 className="place-self-center">{itemData.id + " : " + itemData.name}</h1>
          <img className="place-self-center h-60" src={itemData.icon_large} alt={itemData.icon_large} />
          <h2 className="place-self-center h-20 text-center">{itemData.description}</h2>
        </div>
        <div className="grid grid-cols-2 place-content-center gap-10">
          <CustButton color="green">True</CustButton>
          <CustButton color="red">False</CustButton>
        </div>
        <div className="grid grid-cols-1 place-content-center">
          <CustButton color="indigo" buttonOnClick={getNewItem}>New Item</CustButton>
        </div>
      </div>
    </main>
  )
}
