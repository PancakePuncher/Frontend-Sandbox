"use client"

import CustButton from "@/components/button/CustButton";
import React, { useState, useEffect } from "react";

export default function Home() {

  const [itemData, setItemData] = useState({})

  const getNewItem = () => {
    const res = fetch("https://pancakepuncher-literate-winner-vgj6q66w9wh69w9-8000.preview.app.github.dev/new_item", {
        redirect: "follow",
        method: "GET",
        mode: "cors"
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
      <div className="grid gap-2 place-content-center pt-50 h-96 border">
        <div className="grid place-content-center border">        
          <h1 className="place-self-center border">{itemData.id + " : " + itemData.name}</h1>
          <img className="place-self-center h-60 border" src={itemData.base64_icon_large} alt={itemData.icon_large} />
          <h2 className="place-self-center h-20 text-center border">{itemData.description}</h2>
        </div>
      </div>
      <div className="grid gap-2 place-content-center pt-10 border">
        <div className="grid grid-cols-2 place-content-center gap-10 border">
          <CustButton color="green">True</CustButton>
          <CustButton color="red">False</CustButton>
        </div>
        <div className="grid grid-cols-1 place-content-center border">
          <CustButton color="indigo" buttonOnClick={getNewItem}>New Item</CustButton>
        </div>
      </div>
    </main>
  )
}
