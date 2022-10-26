
let showMoreDP =document.getElementById("showMoreDP");

showMoreDP.addEventListener('click', function(){
    showmoreDPIDs();
})



async function showmoreDPIDs(){
    // evt.preventDefault()
    let url = new URL(window.location.href);
    let departmentIds = url.searchParams.get("departmentIds");
    let alldata = await $.getJSON("https://collectionapi.metmuseum.org/public/collection/v1/search?",{"q":"art", "departmentId": departmentIds });
    
    let allImage = getMultipleRandom(alldata["objectIDs"], 10)
    console.log(allImage)
    const axiosRequests = []
    for (let i = 0; i < allImage.length; i++) {
        axiosRequests.push(axios.get(`https://collectionapi.metmuseum.org/public/collection/v1/objects/${allImage[i]}`));
    }


    const imgResponse = await axios.all(axiosRequests)
    for (let i = 0; i < allImage.length; i++) {
        let image = null;
        let name = null;

        if(imgResponse[i].data["primaryImage"]){
            image = imgResponse[i].data["primaryImage"]
          }else {
            image = "https://www.appliancepartscompany.com/webapp/img/no_image_available.jpeg"
          }
        if (imgResponse[i].data["artistDisplayName"]){
            name = imgResponse[i].data["artistDisplayName"]
          }else {
            name= "Not Listed"
          }

          $('#imgDP').append(`
            <img  class="img-thumbnail" class="card-image" src="${image}"></img>
            <form method="POST" class="messages-like">
            <button class="
              btn 
              btn-sm 
              {{'btn-primary' if objectID in inspirations else 'btn-secondary'}}"
              formaction="/inspiration/${imgResponse[i].data["objectID"]}/add">
      
              <i class="fa fa-paint-brush"></i> 
            </button>
          </form>
          <div class = "caption">
            <h4>Artist Name:</h4>
            <a href="https://www.metmuseum.org/art/collection/search/${imgResponse[i].data["objectID"]}">
            <h4>${name}
            </h4></a>

            <h5>Art Title: </h5>
            <a href="${imgResponse[i].data["objectWikidata_URL"]}">
            <h5>${imgResponse[i].data["title"]}
            </h5></a>
            </div>`
            )
        
        }



    
}


function getMultipleRandom(arr, num) {
    const shuffled = [...arr].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, num);
  }