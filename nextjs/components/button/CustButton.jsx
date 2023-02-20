export default function CustButton({color="indigo", children, buttonOnClick }) {

    const buttonStyles = {
        colors: {
        red: "bg-red-500",
        green: "bg-green-500",
        indigo: "bg-indigo-500"
        }
    }

    return (
        <button type="button" onClick={buttonOnClick} className={`rounded-lg ${buttonStyles.colors[color]}`}>{children}</button>
    );
};