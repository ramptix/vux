import { codeToHtml } from 'https://esm.sh/shiki@1.0.0'

const loader = document.querySelector('#vux-loader div')

const protocol = window.location.protocol == "http:" ? "ws://" : "wss://"
const ws_uri = protocol + window.location.origin.split('//')[1]

let start;
let $ws;
let $heartbeat;

function newWebsocket(isReload = false) {
    start = new Date()
    $ws = new WebSocket(ws_uri)

    $ws.onopen = () => {
        if (isReload)
            return window.location.reload()

        console.info(`[vux] connected. (${(new Date() - start) / 1000}s, since restart)`)
        loader.style.opacity = 0
        loader.style.filter = "blur(5px)"

        $heartbeat = window.setInterval(() => {
            console.log('[vux] heartbeat')
            $ws.send(JSON.stringify({ t: 'heartbeat' }))
        }, 10 * 1000)
    }

    $ws.onclose = (event) => {
        if (event.reason == "server_runtime_error") {
            console.error("[vux] Error on server side (server_runtime_error)")
            window.clearInterval($heartbeat)
            return
        }
        console.error(`[vux] unexpected close. (${event.code}, reason: ${event.reason || null})`)
        console.warn(`[vux] reconnecting...`)
        loader.style.opacity = 1
        loader.style.filter = "blur(0px)"
        newWebsocket(true)
        window.clearInterval($heartbeat)
    }

    $ws.onerror = (event) => {
        console.error('[vux] an error occured.', event)
    }

    $ws.onmessage = ({ "data": rawData }) => {
        const data = JSON.parse(rawData)

        if (data.t == "startup") {
            runStartupScripts(data)
        }
        else if (data.t == "update") {
            runScripts(data)
        }
        else if (data.t == "error") {
            serverSideError(data)
        }
    }
}

newWebsocket()

function generateSnippet(k) {
    return `let $target = document.querySelector(\`[data-control="${k}"]\`)\n`
}

function stateLoading($target) {
    $target.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" 
        viewBox="0 0 24 24" 
        stroke-width="1.5" 
        stroke="currentColor" 
        fill="none" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="vux-loader-svg"    
    >
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
        <path d="M12 6l0 -3"></path>
        <path d="M16.25 7.75l2.15 -2.15"></path>
        <path d="M18 12l3 0"></path>
        <path d="M16.25 16.25l2.15 2.15"></path>
        <path d="M12 18l0 3"></path>
        <path d="M7.75 16.25l-2.15 2.15"></path>
        <path d="M6 12l-3 0"></path>
        <path d="M7.75 7.75l-2.15 -2.15"></path>
    </svg>
    `
    $target.disabled = true
}

function stateDefault($target) {
    $target.disabled = false
}

function runStartupScripts(data) {
    Object.entries(data.d).forEach(([k, v]) => {
        const $target = document.querySelector(`[data-control="${k}"]`)
        const { listens } = Function(
            generateSnippet(k) + v
        )()

        listens.forEach(type => {
            $target.addEventListener(type, (event) => {
                if (listens.includes(event.type)) {
                    stateLoading($target)
                    $ws.send(JSON.stringify({
                        t: 'update',
                        d: {
                            id: k,
                            event: event.type
                        }
                    }))
                }
            })
        })
    })
}

function runScripts(data) {
    const k = Object.keys(data.d)[0]
    const v = data.d[k]

    const $target = document.querySelector(`[data-control="${k}"]`)

    console.log(k, v)
    Function(generateSnippet(k) + v)()
    
    stateDefault($target)
}

async function serverSideError(data) {
    document.getElementById("root").innerHTML = "";

    const modal = document.querySelector('dialog#vux-dialog')
    modal.showModal()

    modal.querySelector("div").innerHTML = (
        `<code>${data.d.sum}</code>` +
        await codeToHtml(
            data.d.err,
            {
                lang: 'js',
                theme: 'aurora-x'
            }
        )
    )
}