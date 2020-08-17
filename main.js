function is_any_empty() {
    var username = document.getElementById("usernameField").value
    var password = document.getElementById("passwordField").value
    var data1 = document.getElementById("hashtags").value
    var data2 = document.getElementById("usernames").value

    // if ((!Boolean(username) || !Boolean(password)) || (!Boolean(data1) && !Boolean(data2))) {
    //     return true;
    // }
    if ((!Boolean(username) || !Boolean(password))) {
        return true;
    }
    return false;
}

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function sub() {
    if (is_any_empty()) {
        Swal.fire({
                icon: 'error',
                title: 'Wrong input',
                text: 'Never Leave any field empty!',
            }).then(() => {
                // var ele = document.getElementById("hastags_or_usernames")
                // ele.value = "#cool,#hot"
            })
            // window.top.close();
    } else {
        var username = document.getElementById("usernameField").value
        var password = document.getElementById("passwordField").value
        var like = document.getElementById("like").checked
        var follow = document.getElementById("follow").checked
        var whitelist_follow = document.getElementById("whitelist_follow").checked
        var unfollow = document.getElementById("unfollow").checked
        var dms = document.getElementById("dm").checked
        target_hashtags = document.getElementById("hashtags").value
        target_usernames = document.getElementById("usernames").value

        likes_per_hour = Number(document.getElementById("likes_per_hour").value)
        follows_per_hour = Number(document.getElementById("follows_per_hour").value)
        whitelist_follows_per_hour = Number(document.getElementById("whitelist_follows_per_hour").value)
        unfollows_per_hour = Number(document.getElementById("unfollows_per_hour").value)
        dms_per_hour = Number(document.getElementById("dms_per_hour").value)




        unfollow_after_x_days = Number(document.getElementById("unfollow_after_x_days").value)
        white_list_users = document.getElementById('set_whitelist').value
        if ((like && !Boolean(target_hashtags))) {
            // || (!like && Boolean(target_hashtags))
            Swal.fire({
                icon: 'error',
                title: 'Like Option is ON, But Target Hashtags not provided',
                showConfirmButton: true
            })
        } else if (((follow || dms) && !Boolean(target_usernames))) {
            // || ((!follow || !dms) && Boolean(target_usernames))
            Swal.fire({
                icon: 'error',
                title: 'Follow/DM Option is ON, But Target Usernames not provided',
                showConfirmButton: true
            })
        } else if ((whitelist_follow && !Boolean(white_list_users))) {
            Swal.fire({
                icon: 'error',
                title: 'whitelist-follow Option is ON, But White-list-users not provided',
                showConfirmButton: true
            })
        } else {
            var mode = "h";

            if (!Boolean(likes_per_hour)) {
                likes_per_hour = 15
            }
            if (!Boolean(follows_per_hour)) {
                follows_per_hour = 10
            }
            if (!Boolean(unfollows_per_hour)) {
                unfollows_per_hour = 15
            }
            if (!Boolean(dms_per_hour)) {
                dms_per_hour = 15
            }
            if (!Boolean(whitelist_follows_per_hour)) {
                whitelist_follows_per_hour = 10
            }

            if (unfollow_after_x_days <= 0) {
                unfollow_after_x_days = 3
            }
            if (!Boolean(white_list_users)) {
                white_list_users = ''
            }

            Swal.fire({
                position: 'mid',
                icon: 'success',
                title: 'Data Push To Bot Successfully!',
                showConfirmButton: false,
                timer: 2000
            })
            sleep(1500).then(() => {
                eel.START_BOT(username, password, target_hashtags, target_usernames, mode, like, follow, unfollow, dms, whitelist_follow, unfollow_after_x_days, white_list_users, likes_per_hour, follows_per_hour, unfollows_per_hour, dms_per_hour, whitelist_follows_per_hour)
                window.top.close();
            });
        }
    }

}

function set_comments() {
    eel.set_comments()
}

function set_dms() {
    eel.set_dms()
}

async function set_whitelist() {
    eel.get_save()(async function(res) {
        if (res) {
            const { value: whiteListUsers } = await Swal.fire({
                title: 'Whitelist users',
                html: `
                            <textarea name="text" id="white_list_users" class="form-control" placeholder='username1,username2,username3...' style="font-size: 20px;" cols="30" rows="2">${res.white_list_users}</textarea>
                        `,
                focusConfirm: false,
                preConfirm: () => {
                    return document.getElementById('white_list_users').value

                }
            })

            if (whiteListUsers) {
                document.getElementById('set_whitelist').value = whiteListUsers
            }
        } else {
            const { value: whiteListUsers } = await Swal.fire({
                title: 'Whitelist users',
                html: `
                            <textarea name="text" id="white_list_users" class="form-control" placeholder='username1,username2,username3...' style="font-size: 20px;" cols="30" rows="2"></textarea>
                        `,
                focusConfirm: false,
                preConfirm: () => {
                    return document.getElementById('white_list_users').value

                }
            })

            if (whiteListUsers) {
                document.getElementById('set_whitelist').value = whiteListUsers
            }
        }
    })


}

function handleClick(myRadio) {
    var ele = document.getElementById("hastags_or_usernames")
    var btn = document.getElementById("start_insta")
    if (myRadio.value == "user") {
        ele.style.visibility = "visible";
        ele.placeholder = "username_1,username_2";
        btn.style.visibility = "visible";
    } else if (myRadio.value == "Hashtag") {
        ele.style.visibility = "visible";
        ele.placeholder = "#new,#hairstyle,#business";
        btn.style.visibility = "visible";
    } else {
        ele.style.visibility = "visible";
        ele.placeholder = "Pakistan,German";
        btn.style.visibility = "visible"
    }

}

function fill_save() {
    eel.get_save()(function(res) {
        if (res) {
            document.getElementById("usernameField").value = res.username
            document.getElementById("passwordField").value = res.password
            document.getElementById("like").checked = res.like
            document.getElementById("follow").checked = res.follow
            document.getElementById("unfollow").checked = res.unfollow
            document.getElementById("unfollow").checked = res.unfollow
            document.getElementById('dm').checked = res.dms
            document.getElementById("likes_per_hour").value = res.likes_per_hour
            document.getElementById("follows_per_hour").value = res.follows_per_hour
            document.getElementById("unfollows_per_hour").value = res.unfollows_per_hour
            document.getElementById("dms_per_hour").value = res.dms_per_hour
            document.getElementById("unfollow_after_x_days").value = res.unfollow_after_x_days
            document.getElementById('set_whitelist').value = res.white_list_users
            document.getElementById("hashtags").value = res.target_hashtags
            document.getElementById("usernames").value = res.target_usernames

            total_actions = res.follows_per_hour + res.unfollows_per_hour + res.dms_per_hour + res.likes_per_hour
            document.getElementById('actions_in_total').value = total_actions
            document.getElementById('actions_in_total_2').value = total_actions * 12


        } else {

        }
    })
}

// per hour change
function like_per_hr_changer() {
    total_f = Number(document.getElementById('follows_per_hour').value)
    total_unf = Number(document.getElementById('unfollows_per_hour').value)
    total_dms = Number(document.getElementById('dms_per_hour').value)
    total_likes = Number(document.getElementById('likes_per_hour').value)
    total_whitelist_follow = Number(document.getElementById('whitelist_follows_per_hour').value)

    if (document.getElementById('follow').checked) {
        if (!Boolean(total_f)) {
            total_f = 10
        }
    } else {
        total_f = 0
    }

    if (document.getElementById('unfollow').checked) {
        if (!Boolean(total_unf)) {
            total_unf = 10
        }
    } else {
        total_unf = 0
    }

    if (document.getElementById('dm').checked) {
        if (!Boolean(total_dms)) {
            total_dms = 10
        }
    } else {
        total_dms = 0
    }

    if (document.getElementById('like').checked) {
        if (!Boolean(total_likes)) {
            total_likes = 10
        }
    } else {
        total_likes = 0
    }

    if (document.getElementById('whitelist_follow').checked) {
        if (!Boolean(total_whitelist_follow)) {
            total_whitelist_follow = 10
        }
    } else {
        total_whitelist_follow = 0
    }

    if (total_likes > 50) {
        Swal.fire({
            icon: 'warning',
            title: 'Likes/hour cannot be increased from 50',
            showConfirmButton: true
        }).then(() => {
            document.getElementById('likes_per_hour').value = 50
            total_likes = 50
            total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
            document.getElementById('actions_in_total').value = total_actions
            document.getElementById('actions_in_total_2').value = total_actions * 12
        })
    } else {
        total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
        document.getElementById('actions_in_total').value = total_actions
        document.getElementById('actions_in_total_2').value = total_actions * 12
    }
}

function follow_per_hour_changer() {
    total_f = Number(document.getElementById('follows_per_hour').value)
    total_unf = Number(document.getElementById('unfollows_per_hour').value)
    total_dms = Number(document.getElementById('dms_per_hour').value)
    total_likes = Number(document.getElementById('likes_per_hour').value)
    total_whitelist_follow = Number(document.getElementById('whitelist_follows_per_hour').value)

    if (document.getElementById('follow').checked) {
        if (!Boolean(total_f)) {
            total_f = 10
        }
    } else {
        total_f = 0
    }

    if (document.getElementById('unfollow').checked) {
        if (!Boolean(total_unf)) {
            total_unf = 10
        }
    } else {
        total_unf = 0
    }

    if (document.getElementById('dm').checked) {
        if (!Boolean(total_dms)) {
            total_dms = 10
        }
    } else {
        total_dms = 0
    }

    if (document.getElementById('like').checked) {
        if (!Boolean(total_likes)) {
            total_likes = 10
        }
    } else {
        total_likes = 0
    }

    if (document.getElementById('whitelist_follow').checked) {
        if (!Boolean(total_whitelist_follow)) {
            total_whitelist_follow = 10
        }
    } else {
        total_whitelist_follow = 0
    }
    if (total_f + total_whitelist_follow > 50) {
        Swal.fire({
            icon: 'warning',
            title: 'follow+whitelist-follow/hour cannot be increased from 50',
            showConfirmButton: true
        }).then(() => {
            document.getElementById('follows_per_hour').value = 25
            document.getElementById('whitelist_follows_per_hour').value = 25
            total_f = 25
            total_whitelist_follow = 25
            total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
            document.getElementById('actions_in_total').value = total_actions
            document.getElementById('actions_in_total_2').value = total_actions * 12
        })
    } else {
        total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
        document.getElementById('actions_in_total').value = total_actions
        document.getElementById('actions_in_total_2').value = total_actions * 12
    }
}

function whitelist_follow_per_hour_changer() {
    total_f = Number(document.getElementById('follows_per_hour').value)
    total_unf = Number(document.getElementById('unfollows_per_hour').value)
    total_dms = Number(document.getElementById('dms_per_hour').value)
    total_likes = Number(document.getElementById('likes_per_hour').value)
    total_whitelist_follow = Number(document.getElementById('whitelist_follows_per_hour').value)

    if (document.getElementById('follow').checked) {
        if (!Boolean(total_f)) {
            total_f = 10
        }
    } else {
        total_f = 0
    }

    if (document.getElementById('unfollow').checked) {
        if (!Boolean(total_unf)) {
            total_unf = 10
        }
    } else {
        total_unf = 0
    }

    if (document.getElementById('dm').checked) {
        if (!Boolean(total_dms)) {
            total_dms = 10
        }
    } else {
        total_dms = 0
    }

    if (document.getElementById('like').checked) {
        if (!Boolean(total_likes)) {
            total_likes = 10
        }
    } else {
        total_likes = 0
    }

    if (document.getElementById('whitelist_follow').checked) {
        if (!Boolean(total_whitelist_follow)) {
            total_whitelist_follow = 10
        }
    } else {
        total_whitelist_follow = 0
    }
    if (total_f + total_whitelist_follow > 50) {
        Swal.fire({
            icon: 'warning',
            title: 'follow+whitelist-follow/hour cannot be increased from 50',
            showConfirmButton: true
        }).then(() => {
            document.getElementById('follows_per_hour').value = 25
            document.getElementById('whitelist_follows_per_hour').value = 25
            total_f = 25
            total_whitelist_follow = 25
            total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
            document.getElementById('actions_in_total').value = total_actions
            document.getElementById('actions_in_total_2').value = total_actions * 12
        })
    } else {
        total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
        document.getElementById('actions_in_total').value = total_actions
        document.getElementById('actions_in_total_2').value = total_actions * 12
    }
}

function unfollow_per_hour_changer() {
    total_f = Number(document.getElementById('follows_per_hour').value)
    total_unf = Number(document.getElementById('unfollows_per_hour').value)
    total_dms = Number(document.getElementById('dms_per_hour').value)
    total_likes = Number(document.getElementById('likes_per_hour').value)
    total_whitelist_follow = Number(document.getElementById('whitelist_follows_per_hour').value)

    if (document.getElementById('follow').checked) {
        if (!Boolean(total_f)) {
            total_f = 10
        }
    } else {
        total_f = 0
    }

    if (document.getElementById('unfollow').checked) {
        if (!Boolean(total_unf)) {
            total_unf = 10
        }
    } else {
        total_unf = 0
    }

    if (document.getElementById('dm').checked) {
        if (!Boolean(total_dms)) {
            total_dms = 10
        }
    } else {
        total_dms = 0
    }

    if (document.getElementById('like').checked) {
        if (!Boolean(total_likes)) {
            total_likes = 10
        }
    } else {
        total_likes = 0
    }

    if (document.getElementById('whitelist_follow').checked) {
        if (!Boolean(total_whitelist_follow)) {
            total_whitelist_follow = 10
        }
    } else {
        total_whitelist_follow = 0
    }
    if (total_unf > 50) {
        Swal.fire({
            icon: 'warning',
            title: 'unfollow/hour cannot be increased from 50',
            showConfirmButton: true
        }).then(() => {
            document.getElementById('unfollows_per_hour').value = 50
            total_unf = 50
            total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
            document.getElementById('actions_in_total').value = total_actions
            document.getElementById('actions_in_total_2').value = total_actions * 12
        })
    } else {
        total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
        document.getElementById('actions_in_total').value = total_actions
        document.getElementById('actions_in_total_2').value = total_actions * 12
    }
}

function dm_per_hour_changer() {
    total_f = Number(document.getElementById('follows_per_hour').value)
    total_unf = Number(document.getElementById('unfollows_per_hour').value)
    total_dms = Number(document.getElementById('dms_per_hour').value)
    total_likes = Number(document.getElementById('likes_per_hour').value)
    total_whitelist_follow = Number(document.getElementById('whitelist_follows_per_hour').value)

    if (document.getElementById('follow').checked) {
        if (!Boolean(total_f)) {
            total_f = 10
        }
    } else {
        total_f = 0
    }

    if (document.getElementById('unfollow').checked) {
        if (!Boolean(total_unf)) {
            total_unf = 10
        }
    } else {
        total_unf = 0
    }

    if (document.getElementById('dm').checked) {
        if (!Boolean(total_dms)) {
            total_dms = 10
        }
    } else {
        total_dms = 0
    }

    if (document.getElementById('like').checked) {
        if (!Boolean(total_likes)) {
            total_likes = 10
        }
    } else {
        total_likes = 0
    }

    if (document.getElementById('whitelist_follow').checked) {
        if (!Boolean(total_whitelist_follow)) {
            total_whitelist_follow = 10
        }
    } else {
        total_whitelist_follow = 0
    }
    if (total_dms > 50) {
        Swal.fire({
            icon: 'warning',
            title: 'dms/hour cannot be increased from 50',
            showConfirmButton: true
        }).then(() => {
            document.getElementById('dms_per_hour').value = 50
            total_dms = 50
            total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
            document.getElementById('actions_in_total').value = total_actions
            document.getElementById('actions_in_total_2').value = total_actions * 12
        })
    } else {
        total_actions = total_f + total_unf + total_dms + total_likes + total_whitelist_follow
        document.getElementById('actions_in_total').value = total_actions
        document.getElementById('actions_in_total_2').value = total_actions * 12
    }
}


$("#likes_per_hour").on('change keydown paste input', like_per_hr_changer);

$("#follows_per_hour").on('change keydown paste input', follow_per_hour_changer);

$("#whitelist_follows_per_hour").on('change keydown paste input', whitelist_follow_per_hour_changer);

$("#unfollows_per_hour").on('change keydown paste input', unfollow_per_hour_changer);

$("#dms_per_hour").on('change keydown paste input', dm_per_hour_changer);



// per enable/disbale
document.getElementById('like').addEventListener('change', function() {
    if (this.checked) {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = false
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 15
    } else {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = true
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 0
    }
    like_per_hr_changer()
});

document.getElementById('follow').addEventListener('change', function() {
    if (this.checked) {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = false
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 10
    } else {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = true
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 0
    }
    follow_per_hour_changer()
});

document.getElementById('whitelist_follow').addEventListener('change', function() {
    if (this.checked) {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = false
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 10
    } else {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = true
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 0
    }
    whitelist_follow_per_hour_changer()
});

document.getElementById('unfollow').addEventListener('change', function() {
    if (this.checked) {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = false
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 15
    } else {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = true
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 0
    }
    unfollow_per_hour_changer()
});

document.getElementById('dm').addEventListener('change', function() {
    if (this.checked) {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = false
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 15
    } else {
        this.parentElement.parentElement.getElementsByTagName('input')[1].disabled = true
        this.parentElement.parentElement.getElementsByTagName('input')[1].value = 0
    }
    dm_per_hour_changer()
});