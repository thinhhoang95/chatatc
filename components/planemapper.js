import { useEffect } from "react"

export default function PlaneMapper({planes}) {

    const utm_to_px = (utm_x, utm_y) => {
        const bottom_left = [530603.5743816729, 1046432.9997519567] // x, y
        const top_right = [830603.5743816729, 1346432.9997519567] // x, y
        const original_width = top_right[0] - bottom_left[0]
        const original_height = top_right[1] - bottom_left[1]

        const canvas_width = 650 // must match canvas width and height defined below
        const canvas_height = 650

        return [
            (utm_x - bottom_left[0]) / original_width * canvas_width,
            (utm_y - bottom_left[1]) / original_height * canvas_height
        ]
    }

    // render canvas when planes is updated
    useEffect(() => {
        // get canvas
        const canvas = document.getElementById("myCanvas");
        const ctx = canvas.getContext("2d");

        // clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // draw planes
        planes.forEach(plane => {
            // draw plane
            const [x, y] = utm_to_px(plane.x, plane.y)
            // draw a square at (x, y)
            ctx.fillStyle = "blue";
            ctx.fillRect(x, y, 10, 10);
            // draw callsign
            ctx.font = "12px Arial";
            ctx.fillStyle = "blue";
            ctx.fillText(plane.callsign, x, y-35);
            // altitude and speed
            ctx.fillText(`${((plane.z)/100).toFixed(0)} ${plane.V.toFixed(0)} ${plane.psi.toFixed(0)}`, x, y-22);
            ctx.fillStyle="red"
            // desired altitude and speed
            ctx.fillText(`${((plane.z_desired)/100).toFixed(0)} ${plane.V_desired.toFixed(0)} ${plane.psi_desired.toFixed(0)}`, x, y-9);
        });
    }, [planes])

    return(
        <canvas id="myCanvas" width="650px" height="650px" style={{background: 'url("./vvts.png")', backgroundSize: "cover"}}>
            Your browser does not support the HTML5 canvas tag.
        </canvas>
    )
}
