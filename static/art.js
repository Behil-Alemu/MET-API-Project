// return search result


const imgIds = document.querySelectorAll("img")
const artist = document.getElementsByClassName("artist-name")
const title = document.getElementsByClassName("artist-title")


async function main() {
    
    const axiosRequests = []
    for (let i = 0; i < imgIds.length; i++) {
        axiosRequests.push(axios.get(`https://collectionapi.metmuseum.org/public/collection/v1/objects/${imgIds[i]['id']}`));
    }
    const imgResponse = await axios.all(axiosRequests)

        for (let i = 0; i < imgIds.length; i++) {
            if (imgResponse[i].data["primaryImageSmall"])
            {
            imgIds[i].src = imgResponse[i].data["primaryImageSmall"]
            }else{
                imgIds[i].src = "https://www.appliancepartscompany.com/webapp/img/no_image_available.jpeg"
            }
            
            if (imgResponse[i].data["artistDisplayName"]){
            artist[i].innerHTML =imgResponse[i].data["artistDisplayName"]
            } 
            if (imgResponse[i].data["title"] ){
            title[i].innerHTML =imgResponse[i].data["title"] 
            }
          
    }
}

main();





