export async function getNewItem() {

    const res = await fetch("https://pancakepuncher-literate-winner-vgj6q66w9wh69w9-8000.preview.app.github.dev/new_item",
        {
            method: "GET",
            mode: "no-cors"
        }
    )

    console.log(res)
    
    return response
}