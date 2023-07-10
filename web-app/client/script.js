var url = "http://127.0.0.1:5000/Recommend_Songs";
function onClick() {
  console.log('Recommend! Clicked');
  var id = document.getElementById("playlist-id").value;
  var numberSongs = document.getElementById("number-songs").value;
  console.log(id);
  console.log(numberSongs);

  recommendationTable = document.getElementById("recommendation-table")

  $.post(url, {
      id: id,
      num_songs: parseFloat(numberSongs)
      },
      function(data, status) {
      console.log(data.recommendations);
      recommendationTable.innerHTML = data.recommendations;
      console.log(status);
      });

}
