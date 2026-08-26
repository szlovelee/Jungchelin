document.addEventListener("DOMContentLoaded", function () {
    const restaurantForm = document.querySelector(
        '#restaurantModal form[action="/restaurants"]'
    );

    const reviewForm = document.querySelector(
        'form[action="/reviews"]'
    );

    const pinButtons = document.querySelectorAll(
        ".pin-button"
    );


    // 고정핀 클릭
    pinButtons.forEach(function (pinButton) {
        pinButton.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();
            
            const response = await fetch(`/restaurants/${restaurantId}/pin`, {
                method: "POST"
            });

            const isPinned = await response.json()

            pinButton.setAttribute(
                "aria-pressed",
                String(isPinned)
            );
        });
    });


    // 식당 등록 검증
    if (restaurantForm) {
        restaurantForm.addEventListener("submit", function (event) {
            const nameInput = restaurantForm.querySelector(
                'input[name="name"]'
            );

            const categorySelect = restaurantForm.querySelector(
                'select[name="category"]'
            );

            const addressInput = restaurantForm.querySelector(
                'input[name="addr"]'
            );

            if (!nameInput || !categorySelect || !addressInput) {
                return;
            }

            if (!nameInput.value.trim()) {
                event.preventDefault();
                alert("식당 이름을 입력해주세요.");
                nameInput.focus();
                return;
            }

            if (!categorySelect.value.trim()) {
                event.preventDefault();
                alert("식당 분류를 선택해주세요.");
                categorySelect.focus();
                return;
            }

            if (!addressInput.value.trim()) {
                event.preventDefault();
                alert("식당 주소를 입력해주세요.");
                addressInput.focus();
            }
        });
    }


    // 리뷰 등록 검증
    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            const commentInput = reviewForm.querySelector(
                'input[name="comment"]'
            );

            const starSelect = reviewForm.querySelector(
                'select[name="star"]'
            );

            if (!commentInput || !starSelect) {
                return;
            }

            if (!commentInput.value.trim()) {
                event.preventDefault();
                alert("한줄평을 입력해주세요.");
                commentInput.focus();
                return;
            }

            if (!starSelect.value) {
                event.preventDefault();
                alert("별점을 선택해주세요.");
                starSelect.focus();
            }
        });
    }
});