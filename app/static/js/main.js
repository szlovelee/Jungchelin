document.addEventListener("DOMContentLoaded", function () {
    const restaurantForm =
        document.getElementById("restaurantForm");

    const reviewForm =
        document.querySelector('form[action="/reviews"]');

    const pinButtons =
        document.querySelectorAll(".pin-button");

    const duplicateError =
        document.getElementById("restaurantDuplicateError");


    // 고정핀 클릭
    // 현재 핀 서버는 JSON이 아니라 redirect를 반환하므로 form을 제출한다.
    pinButtons.forEach(function (pinButton) {
        pinButton.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();

            const pinForm = pinButton.closest("form");

            if (pinForm) {
                pinForm.submit();
            }
        });
    });


    // 식당 중복 안내 문구 숨기기
    function hideDuplicateError() {
        if (!duplicateError) {
            return;
        }

        duplicateError.classList.add("d-none");
        duplicateError.textContent = "";
    }


    // 입력값을 수정하면 기존 중복 안내 문구 숨기기
    if (restaurantForm) {
        const restaurantInputs =
            restaurantForm.querySelectorAll(
                'input[name="name"], ' +
                'select[name="category"], ' +
                'input[name="addr"], ' +
                'input[name="main_menu"]'
            );

        restaurantInputs.forEach(function (input) {
            const eventName =
                input.tagName === "SELECT"
                    ? "change"
                    : "input";

            input.addEventListener(
                eventName,
                hideDuplicateError
            );
        });
    }


    // 식당 등록
    if (restaurantForm) {
        restaurantForm.addEventListener(
            "submit",
            async function (event) {
                event.preventDefault();

                const nameInput =
                    restaurantForm.querySelector(
                        'input[name="name"]'
                    );

                const categorySelect =
                    restaurantForm.querySelector(
                        'select[name="category"]'
                    );

                const addressInput =
                    restaurantForm.querySelector(
                        'input[name="addr"]'
                    );

                const submitButton =
                    restaurantForm.querySelector(
                        'button[type="submit"]'
                    );

                hideDuplicateError();

                if (
                    !nameInput ||
                    !categorySelect ||
                    !addressInput
                ) {
                    alert(
                        "식당 등록 입력칸을 찾을 수 없습니다."
                    );
                    return;
                }

                if (!nameInput.value.trim()) {
                    alert("식당 이름을 입력해주세요.");
                    nameInput.focus();
                    return;
                }

                if (!categorySelect.value.trim()) {
                    alert("식당 분류를 선택해주세요.");
                    categorySelect.focus();
                    return;
                }

                if (!addressInput.value.trim()) {
                    alert("식당 주소를 입력해주세요.");
                    addressInput.focus();
                    return;
                }

                if (submitButton) {
                    submitButton.disabled = true;
                }

                try {
                    const response = await fetch(
                        restaurantForm.action,
                        {
                            method: "POST",
                            body: new FormData(
                                restaurantForm
                            ),
                            headers: {
                                "X-Requested-With":
                                    "XMLHttpRequest"
                            }
                        }
                    );

                    const result =
                        await response.json();

                    if (
                        !response.ok ||
                        !result.success
                    ) {
                        if (
                            result.code ===
                            "DUPLICATE_RESTAURANT"
                        ) {
                            const message =
                                result.msg ||
                                "이미 등록된 식당입니다.";

                            alert(message);

                            if (duplicateError) {
                                duplicateError.textContent =
                                    message;

                                duplicateError.classList.remove(
                                    "d-none"
                                );
                            }

                            addressInput.focus();
                        } else {
                            alert(
                                result.msg ||
                                "식당 등록에 실패했습니다."
                            );
                        }

                        // 모달과 입력값을 그대로 유지한다.
                        return;
                    }

                    const modalElement =
                        document.getElementById(
                            "restaurantModal"
                        );

                    if (modalElement) {
                        const modal =
                            bootstrap.Modal
                                .getOrCreateInstance(
                                    modalElement
                                );

                        modal.hide();
                    }

                    window.location.href = "/home";

                } catch (error) {
                    console.error(error);

                    alert(
                        "서버와 통신하는 중 문제가 발생했습니다."
                    );
                } finally {
                    if (submitButton) {
                        submitButton.disabled = false;
                    }
                }
            }
        );
    }


    // 리뷰 등록 검증
    if (reviewForm) {
        reviewForm.addEventListener(
            "submit",
            function (event) {
                const commentInput =
                    reviewForm.querySelector(
                        'input[name="comment"]'
                    );

                const starSelect =
                    reviewForm.querySelector(
                        'select[name="star"]'
                    );

                if (
                    !commentInput ||
                    !starSelect
                ) {
                    return;
                }

                if (!commentInput.value.trim()) {
                    event.preventDefault();

                    alert(
                        "한줄평을 입력해주세요."
                    );

                    commentInput.focus();
                    return;
                }

                if (!starSelect.value) {
                    event.preventDefault();

                    alert(
                        "별점을 선택해주세요."
                    );

                    starSelect.focus();
                }
            }
        );
    }
});