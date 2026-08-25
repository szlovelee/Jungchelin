// app/static/js/main.js

document.addEventListener("DOMContentLoaded", function () {
    const restaurantModal = document.getElementById("restaurant-modal");
    const restaurantForm = document.querySelector(".restaurant-form");
    const reviewForm = document.querySelector(".review-form");

    // 식당 추가 모달 열기
    window.openRestaurantModal = function () {
        if (!restaurantModal) {
            return;
        }

        restaurantModal.classList.add("active");
        document.body.style.overflow = "hidden";
    };

    // 식당 추가 모달 닫기
    window.closeRestaurantModal = function () {
        if (!restaurantModal) {
            return;
        }

        restaurantModal.classList.remove("active");
        document.body.style.overflow = "auto";
    };

    // 모달 바깥쪽 클릭하면 닫기
    if (restaurantModal) {
        restaurantModal.addEventListener("click", function (event) {
            if (event.target === restaurantModal) {
                closeRestaurantModal();
            }
        });
    }

    // ESC 키 누르면 모달 닫기
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeRestaurantModal();
        }
    });

    // 식당 추가 form 간단 검증
    if (restaurantForm) {
        restaurantForm.addEventListener("submit", function (event) {
            const nameInput = restaurantForm.querySelector('input[name="name"]');
            const categorySelect = restaurantForm.querySelector('select[name="category"]');
            const addressInput = restaurantForm.querySelector('input[name="address"]');

            const name = nameInput.value.trim();
            const category = categorySelect.value.trim();
            const address = addressInput.value.trim();

            if (!name) {
                event.preventDefault();
                alert("식당 이름을 입력해주세요.");
                nameInput.focus();
                return;
            }

            if (!category) {
                event.preventDefault();
                alert("식당 분류를 선택해주세요.");
                categorySelect.focus();
                return;
            }

            if (!address) {
                event.preventDefault();
                alert("식당 주소를 입력해주세요.");
                addressInput.focus();
                return;
            }
        });
    }

    // 리뷰 등록 form 간단 검증
    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            const commentInput = reviewForm.querySelector('input[name="comment"]');
            const ratingSelect = reviewForm.querySelector('select[name="rating"]');

            const comment = commentInput.value.trim();
            const rating = ratingSelect.value;

            if (!comment) {
                event.preventDefault();
                alert("한줄평을 입력해주세요.");
                commentInput.focus();
                return;
            }

            if (!rating) {
                event.preventDefault();
                alert("별점을 선택해주세요.");
                ratingSelect.focus();
                return;
            }
        });
    }
});