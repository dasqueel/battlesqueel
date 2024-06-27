function deleteBeatWriter(beatWriter, team) {
	const url = new URL("http://127.0.0.1:5000/beatWriters");
	const params = { team, beatWriter };
	url.search = new URLSearchParams(params).toString();

	fetch(url, { method: "DELETE" })
		.then((response) => {
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.text();
		})
		.then((data) => {
		if (data === "success") {
			alert("removed beat writer");
		} else {
			alert("didnt remove beat writer");
		}
		})
		.catch((error) => {
		console.error(
			"There has been a problem with your fetch operation:",
			error
		);
		});
  }

function deleteNote(note, team, elementId) {
	const url = new URL("http://127.0.0.1:5000/notes");
	const params = { team, note };
	url.search = new URLSearchParams(params).toString();

	fetch(url, { method: "DELETE" })
	.then((response) => {
		if (!response.ok) {
		throw new Error("Network response was not ok");
		}
		return response.text();
	})
	.then((data) => {
		if (data === "success") {
		const element = document.getElementById(elementId);
		if (element) {
			element.parentNode.removeChild(element);
		}
		} else {
		alert("nope sorry");
		}
	})
	.catch((error) => {
		console.error(
		"There has been a problem with your fetch operation:",
		error
		);
	});
}
  
function changeFileName(filename) {
  if (confirm("Are you sure you want to proceed?")) {
    let parts = filename.split('/');
    let cleanFilename = parts.slice(1).join('/');
    const url = new URL(`https://manatee-clever-ray.ngrok-free.app/changeFileName/${cleanFilename}`);

    fetch(url, { method: "POST" })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })  
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      });
  } else {
    console.log("Action cancled")
  }
}

document.addEventListener("DOMContentLoaded", function() {
  var notesTriggers = document.querySelectorAll(".notesTrigger");

  notesTriggers.forEach(function(trigger) {
      var id = trigger.id.replace('notesTrigger', '');
      var notesModal = document.getElementById('notesModal' + id);

      trigger.addEventListener("mouseover", function() {
          notesModal.style.display = "block";
      });

      trigger.addEventListener("mouseout", function() {
          notesModal.style.display = "none";
      });

      notesModal.addEventListener("mouseover", function() {
          notesModal.style.display = "block";
      });

      notesModal.addEventListener("mouseout", function() {
          notesModal.style.display = "none";
      });
  });
});
