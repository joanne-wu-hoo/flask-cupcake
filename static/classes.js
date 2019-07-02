// "parent" ul for individual li cupcakes
// const $cupcakes = $('#cupcakes');

// $(async function() {
//     let response = await axios.get('/cupcakes')
//     let cupcakes = response.data.response
    
//     for (let i = 0; i < cupcakes.length; i++) {
//         let cupcake = cupcakes[i];
//         let $cupcake = $(`
//             <li class="cupcake">
//                 <img src="${cupcake.image}" class="cupcake-img">
//                 <p>Size: ${cupcake.size}</p>
//                 <p>Flavor: ${cupcake.flavor}</p>
//                 <p>Rating: ${cupcake.rating}</p>
//             </li>
//         `);
//         $cupcakes.append($cupcake);
//     }
// })
$(async function() {
    cupcakeList = new CupcakeList($('#cupcakes'));
    debugger;
    cupcakes = await CupcakeList.fetchAllCupcakes();
    debugger;
    cupcakeList.createCupcakes(cupcakes);
})


class CupcakeList {
    constructor(parent){
        this.$parent = parent;
    }
    
    static async fetchAllCupcakes(){
        /* Make an AJAX request to retrieve all cupcakes. Returns list of Cupcake objects {flavor: , size: , image: } */
        let response = await axios.get('/cupcakes');
        let cupcakes = response.data.response;
        return cupcakes;
    }

    createCupcakes(cupcakes){
        /* Given cupcake objects, add information to app */
        for (let i = 0; i < cupcakes.length; i++) {
            let cupcake = cupcakes[i];
            let $cupcake = $(`
                <li class="cupcake">
                    <img src="${cupcake.image}" class="cupcake-img">
                    <p>Size: ${cupcake.size}</p>
                    <p>Flavor: ${cupcake.flavor}</p>
                    <p>Rating: ${cupcake.rating}</p>
                </li>
            `);
            this.$parent.append($cupcake);
        }
    }
}