const $cupcakes = $('#cupcakes');
const $searchForm = $('#search-form')

$(async function() {
    cupcakes = await CupcakeList.fetchAllCupcakesFrom("/cupcakes");
    appendCupcakesToDOM(cupcakes, $cupcakes);

    $searchForm.on('submit', async function(evt){
        evt.preventDefault();
        filtered_cupcakes = await CupcakeList.fetchAllCupcakesFrom("/search");
        // update DOM with cupcakes that match search term
        $cupcakes.empty()
        appendCupcakesToDOM(filtered_cupcakes, $cupcakes);
        
    })

})



class CupcakeList {
    constructor(parent){
        this.$parent = parent; // parent ul to contain individual cupcake li's
    }
    
    static async fetchAllCupcakesFrom(resource){
        /* Make an AJAX request to retrieve all cupcakes from resource (/search, /cupcakes). Returns list of Cupcake objects {flavor: , size: , image: } */
        let response = await axios.get(resource);
        let cupcakes = response.data.response;
        return cupcakes;
    }

    // static async fetchFilteredCupcakes(){
    //     /* Make an AJAX request to retrieve */
    //     let response = await axios.get('/search');
    //     let filtered_cupcakes = response.data.response;
    //     return filtered_cupcakes;
    // }
}

/// HTML UI functions

function appendCupcakesToDOM(cupcakes, $parent){
    /* Given cupcake objects, append an li for each cupcake */
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
        $parent.append($cupcake);
    }
}