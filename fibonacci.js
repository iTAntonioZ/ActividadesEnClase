function fibonacci(n) {
    let a = 0, b = 1;

    for (let i = 0; i < n; i++) {
        console.log(a);

        let temp = a;
        a = b;
        b = temp + b;
    }
}

const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Ingresa un número: ", (respuesta) => {
    const n = parseInt(respuesta);

    fibonacci(n);

    rl.close();
});