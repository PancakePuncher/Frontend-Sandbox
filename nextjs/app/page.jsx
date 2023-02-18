import CustButton from "@/components/button/CustButton";

export default function Home() {

  return (
    <main>
      <div className="grid gap-2 place-content-center h-96 mt-50">
        <div className="grid place-content-center">        
          <h1 className="place-self-center"></h1>
          <img className="place-self-center" src="" alt="" />
          <h2 className="place-self-center">Test</h2>
        </div>
        <div className="grid grid-cols-2 place-content-center gap-10">
          <CustButton color="green">True</CustButton>
          <CustButton color="red">False</CustButton>
        </div>
        <div className="grid grid-cols-1 place-content-center">
          <CustButton color="indigo" onClickAction="getNewItem">New Item</CustButton>
        </div>
      </div>
    </main>
  )
}
